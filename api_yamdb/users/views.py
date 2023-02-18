from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from users.models import User
from users.permissions import IsAdministrator
from users.serializers import (RegestrationTokenSerializer,
                               SignUpUserSerializer, UserAdminSerializer,
                               UserNoAdminSerializer)
from users.utils import send_email


class UserView(viewsets.ModelViewSet):
    """
    Вью-функция.
    Получение данных о пользователе, его создание админом.
    Также возможность редактирования своего
    профиля полльзователем и админом.
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (IsAuthenticated, IsAdministrator,)
    filter_backends = [filters.SearchFilter]
    search_fields = ("username",)
    lookup_field = "username"

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def get_or_patch(self, request):
        if request.user.is_admin:
            serializer = UserAdminSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
        else:
            serializer = UserNoAdminSerializer(
                request.user,
                data=request.data,
                partial=True,
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.method == "GET":
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetTokenView(APIView):
    """
    Вью-функция.
    Получение токена по логину и email.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = RegestrationTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = get_object_or_404(User, username=data['username'])
        if user is None:
            return Response(
                {'username': 'Пользователь с логином не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if data['confirmation_code'] == user.confirmation_code:
            token = AccessToken.for_user(user)
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"confirmation_code": 'Введен неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class SignUpView(APIView):
    """
    Вью-функция.
    Регистрация пользователя.
    """
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = SignUpUserSerializer(data=request.data,)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = {
            "email_subject": "Пользователь успешно создан",
            "email_body": f"Код подтверждения {user.confirmation_code}",
            "email_to": user.email
        }
        send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
