import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate_username(name):
    """
    Проверка логина пользователя.
    """
    if name == 'me':
        raise ValidationError(
            f'Пользователь с таким логином {name} не может создан',
            params={'name': name}
        )
    if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', name) is None:
        raise ValidationError(
            'Логин должен содержать только буквы и цифры',
            params={'name': name}
        )


def validate_email_check(email):
    """
    Проверка email пользователя.
    """
    try:
        validate_email(email)
        return True
    except TypeError as error:
        raise (f'{error}: введён не корректный email адрес')
