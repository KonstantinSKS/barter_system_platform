from django.contrib import admin

from .models import Category, Ad, ExchangeProposal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
    )
    search_fields = ('title',)
    search_help_text = "Поиск по заголовку категории"
    list_filter = ('title',)
    list_display_links = ('title',)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'category',
        'condition',
        'user',
    )
    search_fields = ('title', 'category__title',)
    search_help_text = "Поиск по заголовку объявления и по заголовку категории"
    list_filter = ('title', 'category__title', 'user__username',)
    list_display_links = ('title',)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'sender_ad',
        'receiver_ad',
        'status',
        'created_at',
    )
    search_fields = ('ad_sender__title', 'ad_receiver__title',)
    search_help_text = "Поиск по заголовку объявления"
    list_filter = ('ad_sender__title', 'ad_receiver__title', 'status',)
    list_display_links = ('sender_ad', 'receiver_ad',)

    def sender_ad(self, obj):
        try:
            return obj.ad_sender.title
        except AttributeError:
            return "данных не найдено/больше не существует"
    sender_ad.short_description = "Объявление отправителя"

    def receiver_ad(self, obj):
        try:
            return obj.ad_receiver.title
        except AttributeError:
            return "данных не найдено/больше не существует"
    receiver_ad.short_description = "Объявление получателя"
