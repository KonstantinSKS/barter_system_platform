from django.contrib.auth.models import AbstractUser
from django.db import models

from config import constants


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Логин',
        max_length=constants.USER_CHAR_LENGTH,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Почта',
        max_length=constants.EMAIL_MAX_LENGTH,
        unique=True
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=constants.USER_CHAR_LENGTH
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='pair username/email should be unique'),
        ]

    def __str__(self):
        return self.username
