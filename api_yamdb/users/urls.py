from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import GetTokenView, SignUpView, UserView

app_name = 'users'
router_users = DefaultRouter()

router_users.register(r"users", UserView, basename="users")
# URL для получения информации о пользователях


urlpatterns = [
    path('auth/signup/', SignUpView.as_view(), name="signup"),
    # URL для регистрации пользователя
    path('auth/token/', GetTokenView.as_view(), name="get_token"),
    # URL для афнтификации пользователя
    path('', include(router_users.urls)),
    # Роутер users
]
