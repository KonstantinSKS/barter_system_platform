import pytest
from ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
def test_category_str(category):
    """Проверяет корректность строкового представления категории."""

    assert str(category) == category.title


@pytest.mark.django_db
def test_ad_str_representation(user, category):
    """Проверяет строковое представление объявления Ad."""

    ad = Ad.objects.create(
        title="Телефон",
        description="Почти новый",
        user=user,
        category=category,
        condition="new"
    )
    assert str(ad) == f"Товар: {ad.title}, категория: {category.title}"


@pytest.mark.django_db
def test_exchange_proposal_str(user, another_user, category):
    """Проверяет строковое представление предложения обмена."""

    ad1 = Ad.objects.create(
        title='Книга', description='...', user=user,
        category=category, condition='used'
    )
    ad2 = Ad.objects.create(
        title='Лего', description='...', user=another_user,
        category=category, condition='new'
    )
    proposal = ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2)
    assert 'Объявление отправителя: Книга' in str(proposal)


@pytest.mark.django_db
def test_exchange_proposal_uniqueness(user, another_user, category):
    """Проверяет уникальность пары ad_sender/ad_receiver в ExchangeProposal."""

    ad1 = Ad.objects.create(
        title='Телефон', description='...',
        user=user, category=category, condition='used'
    )
    ad2 = Ad.objects.create(
        title='Наушники', description='...',
        user=another_user, category=category, condition='new'
    )

    ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2)

    with pytest.raises(Exception):
        ExchangeProposal.objects.create(ad_sender=ad1, ad_receiver=ad2)
