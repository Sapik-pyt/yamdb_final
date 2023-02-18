from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

app_name = 'api'

router_reviews = DefaultRouter()

router_reviews.register(r'genres', GenreViewSet, basename='genres')
# URL для получения информации о жанрах
router_reviews.register(r'categories', CategoryViewSet, basename='categories')
# URL для получения информации о категориях
router_reviews.register(r'titles', TitleViewSet, basename='titels')
# URL для получения информации о произведениях
router_reviews.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
# URL для получения информации об отзывах к произедениям
router_reviews.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
# URL для получения информации о комментариях к отзывам

urlpatterns = [
    path('', include(router_reviews.urls)),
    # Роутер reviews
]
