import pytest
from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
def test_registration_view(api_client):
    """Проверяет регистрацию нового пользователя через API."""

    response = api_client.post('/api/registration/', {
        'username': 'newuser',
        'email': 'newuser@mail.com',
        'password': 'NewPass123!'
    })
    assert response.status_code == 201
    assert response.data['username'] == 'newuser'


@pytest.mark.django_db
def test_login_view(user, api_client):
    """Проверяет логин пользователя и получение токена."""

    response = api_client.post('/api/login/', {
        'username': user.username,
        'password': '12345678'
    })
    assert response.status_code == 200
    assert 'token' in response.data


@pytest.mark.django_db
def test_me_view(auth_client, user):
    """Проверяет возврат информации о текущем пользователе (GET /me/)."""

    response = auth_client.get('/api/me/')
    assert response.status_code == 200
    assert response.data['username'] == user.username


@pytest.mark.django_db
def test_create_and_list_ads(auth_client, category):
    """Проверяет создание объявления и последующее получение его в списке."""

    post_data = {
        'title': 'Пианино',
        'description': 'Старинное',
        'category': category.id,
        'condition': 'used'
    }
    post_response = auth_client.post('/api/ads/', data=post_data)
    assert post_response.status_code == 201

    list_response = auth_client.get('/api/ads/')
    assert list_response.status_code == 200
    assert any(ad['title'] == 'Пианино' for ad in list_response.data['results'])


@pytest.mark.django_db
def test_create_and_update_proposal(
        auth_client, another_auth_client, user, another_user, category):
    """Проверяет создание предложения и обновление его статуса другим пользователем."""

    ad_sender = Ad.objects.create(
        title='Сумка', description='...',
        user=user, category=category, condition='used'
    )
    ad_receiver = Ad.objects.create(
        title='Книга', description='...',
        user=another_user, category=category, condition='new'
    )

    response = auth_client.post('/api/proposals/', {
        'ad_sender': ad_sender.id,
        'ad_receiver': ad_receiver.id,
        'comment': 'Обмен?'
    })
    assert response.status_code == 201
    proposal_id = response.data['id']

    patch_response = another_auth_client.patch(f'/api/proposals/{proposal_id}/', {
        'status': 'approved'
    })
    assert patch_response.status_code == 200
    assert patch_response.data['status'] == 'approved'


@pytest.mark.django_db
def test_delete_proposal(auth_client, user, another_user, category):
    """Проверяет удаление предложения обмена автором."""

    ad1 = Ad.objects.create(
        title='А', description='...',
        user=user, category=category, condition='used'
    )
    ad2 = Ad.objects.create(
        title='Б', description='...',
        user=another_user, category=category, condition='new'
    )
    proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2)

    response = auth_client.delete(f'/api/proposals/{proposal.id}/')
    assert response.status_code == 204
