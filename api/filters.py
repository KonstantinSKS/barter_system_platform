import django_filters
from django.utils.functional import lazy

from ads.models import Ad, Category, ExchangeProposal
from users.models import User
from ads import choices as chcs


def generate_ads_categories_label():
    """Динаическая генерация доступных заголовков модели Category
    для AdFilter (отложенный вызов через lazy)."""

    try:
        categories = Category.objects.all()
        titles = [category.title for category in categories]
        return (
            "Для фильтрации по категории выберите один из доступных заголовков"
            "и вставьте его в поле 'category'.<br>"
            f"<b>Доступные заголовки:</b> {', '.join(titles)}"
        )
    except Exception:
        return "Чтобы выполнить фильтрацию по категории, выберите один из доступных заголовков."


class AdFilter(django_filters.FilterSet):
    """Кастомный фильтр для модели Ad.
    Фильтрация по полям category и condition."""

    category = django_filters.ModelChoiceFilter(
        field_name='category__title',
        to_field_name='title',
        queryset=Category.objects.all(),
        label=lazy(generate_ads_categories_label, str)()
    )
    condition = django_filters.ChoiceFilter(
        choices=chcs.AD_CONDITION_CHOICES,
        label='Фильтрация по состоянию товара'
    )

    class Meta:
        model = Ad
        fields = [
            'category',
            'condition',
            ]


class ExchangeProposalFilter(django_filters.FilterSet):
    """Кастомный фильтр для модели ExchangeProposal.
    Фильтрация по отправителю, получателю и полю status."""

    sender_user = django_filters.ModelChoiceFilter(
        field_name='ad_sender__user',
        queryset=User.objects.all(),
        label='Пользователь, отправивший предложение'
    )
    receiver_user = django_filters.ModelChoiceFilter(
        field_name='ad_receiver__user',
        queryset=User.objects.all(),
        label='Пользователь, получивший предложение'
    )
    status = django_filters.ChoiceFilter(
        choices=chcs.PROPOSAL_STATUS_CHOICES,
        label='Фильтрация по статусу предложения'
    )

    class Meta:
        model = ExchangeProposal
        fields = [
            'sender_user',
            'receiver_user',
            'status',
            ]
