import pytest
from rest_framework.test import APIRequestFactory
from api.serializers import (
    UserSignUpSerializer, UserLoginSerializer,
    AdCreateSerializer, AdReadSerializer,
    ProposalCreateSerializer, ProposalUpdateSerializer
)
from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
def test_user_signup_serializer():
    """Проверяет создание нового пользователя через сериализатор регистрации."""

    data = {
        'username': 'testuser',
        'email': 'test@mail.com',
        'password': 'StrongPass123!'
    }
    serializer = UserSignUpSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == data['username']


@pytest.mark.django_db
def test_user_login_serializer(user):
    """Проверяет валидацию данных для входа через UserLoginSerializer."""

    data = {'username': user.username, 'password': '12345678'}
    serializer = UserLoginSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data['user'] == user


@pytest.mark.django_db
def test_valid_ad_create_serializer(user, category):
    """Проверяет создание объявления через AdCreateSerializer."""

    request = APIRequestFactory().post('/ads/')
    request.user = user
    data = {
        'title': 'Игрушка',
        'description': 'Для детей',
        'category': category.id,
        'condition': 'new'
    }
    serializer = AdCreateSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    ad = serializer.save(user=user)
    assert ad.title == 'Игрушка'


@pytest.mark.django_db
def test_ad_read_serializer(user, category):
    """Проверяет вложенные поля user и category в AdReadSerializer."""

    ad = Ad.objects.create(
        title='Ноутбук', description='Скоростной',
        user=user, category=category, condition='new'
    )
    serializer = AdReadSerializer(instance=ad)
    data = serializer.data
    assert data['user'] == user.username
    assert data['category']['title'] == category.title


@pytest.mark.django_db
def test_proposal_create_serializer(user, another_user, category):
    """Проверяет создание предложения обмена через ProposalCreateSerializer."""

    ad_sender = Ad.objects.create(
        title='Книга', description='...',
        user=user, category=category, condition='used'
    )
    ad_receiver = Ad.objects.create(
        title='Лего', description='...', user=another_user,
        category=category, condition='new'
    )
    request = APIRequestFactory().post('/proposals/')
    request.user = user
    data = {'ad_sender': ad_sender.id, 'ad_receiver': ad_receiver.id, 'comment': 'Обменяемся?'}
    serializer = ProposalCreateSerializer(data=data, context={'request': request})
    assert serializer.is_valid(), serializer.errors
    proposal = serializer.save()
    assert proposal.ad_sender == ad_sender


@pytest.mark.django_db
def test_proposal_update_serializer(user, another_user, category):
    """Проверяет изменение статуса предложения через ProposalUpdateSerializer."""

    ad_sender = Ad.objects.create(
        title='Смартфон', description='...',
        user=user, category=category, condition='used'
    )
    ad_receiver = Ad.objects.create(
        title='Гарнитура', description='...',
        user=another_user, category=category, condition='new'
    )
    proposal = ExchangeProposal.objects.create(ad_sender=ad_sender, ad_receiver=ad_receiver)
    data = {'status': 'approved'}
    serializer = ProposalUpdateSerializer(instance=proposal, data=data)
    assert serializer.is_valid(), serializer.errors
    updated = serializer.save()
    assert updated.status == 'approved'
