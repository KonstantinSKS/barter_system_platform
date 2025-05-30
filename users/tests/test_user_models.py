import pytest


@pytest.mark.django_db
def test_user_str(user):
    """Проверяет строковое представление пользователя (username)."""

    assert str(user) == user.username
