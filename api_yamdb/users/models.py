import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_email_check, validate_username

USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """
    Кастомная модель пользователя.
    """
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,),
        blank=False,
        null=False
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        validators=(validate_email_check,),
        blank=False,
        null=False,
    )
    is_active = models.BooleanField(default=True,)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        "Роль",
        max_length=50,
        choices=ROLES,
        default=USER,
        blank=True
    )
    confirmation_code = models.CharField(
        "Код подтверждения",
        max_length=255,
        null=True,
        blank=False,
        default=uuid.uuid4,
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ("id",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"Пользователь - {self.username}"
