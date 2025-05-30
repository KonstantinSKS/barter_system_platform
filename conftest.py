import pytest
from rest_framework.test import APIClient
from users.models import User
from ads.models import Category
from rest_framework.authtoken.models import Token


@pytest.fixture
def user():
    """Создаёт и возвращает пользователя testuser."""

    return User.objects.create_user(
        username='testuser',
        email='test@mail.com',
        password='12345678'
    )


@pytest.fixture
def another_user():
    """Создаёт и возвращает второго пользователя anotheruser."""

    return User.objects.create_user(
        username='anotheruser',
        email='another@mail.com',
        password='87654321'
    )


@pytest.fixture
def category():
    """Создаёт и возвращает категорию 'Книги'."""

    return Category.objects.create(
        title='Книги',
        description='Художественные книги'
    )


@pytest.fixture
def api_client():
    """Возвращает DRF APIClient без авторизации."""

    return APIClient()


@pytest.fixture
def auth_client(user):
    """Возвращает DRF APIClient с токеном авторизации для user."""

    client = APIClient()
    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def another_auth_client(another_user):
    """Возвращает DRF APIClient с токеном авторизации для another_user."""

    client = APIClient()
    token, _ = Token.objects.get_or_create(user=another_user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client
