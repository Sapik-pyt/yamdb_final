from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .mixins import ModelMixinSet
from .permissions import (IsAdminOrReadonly, IsAuthorOrReadOnly,
                          IsModerOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSerializerUpdate)


class GenreViewSet(ModelMixinSet):
    """
    Вью-функция.
    Получение, добавление и удаление жанров
    """
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadonly or IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(ModelMixinSet):
    """
    Вью-функция.
    Получение, добавление и удаление
    информация о категориях
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadonly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Вью-функция.
    Получение, добавление, редактированние
    и удаление информации о произведениях
    и их оценка
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).select_related('category').prefetch_related('genre')
    permission_classes = (IsAdminOrReadonly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'retrieve',):
            return TitleSerializer
        return TitleSerializerUpdate


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Вью-функция.
    Получение, добавление, редактированние
    и удаление отзыва
    """
    serializer_class = ReviewSerializer
    permission_classes = (
        IsModerOrReadOnly | IsAuthorOrReadOnly
        or IsAdminOrReadonly,
    )

    def get_title_object(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title_object().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title_object()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    Вью-функция.
    Получение, добавление, редактированние
    и удаление комментария к отзывам
    """
    serializer_class = CommentSerializer
    permission_classes = (
        IsModerOrReadOnly | IsAuthorOrReadOnly
        or IsAdminOrReadonly,
    )

    def get_rewiew_object(self):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_rewiew_object().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_rewiew_object()
        )
