import os

from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from config import constants
from ads import choices as chcs
from users.models import User


class AbstractModel(models.Model):
    """Абстрактная модель.
    Добавляет заголовок и описание."""

    title = models.CharField(
        max_length=constants.MAX_CHAR_LENGTH,
        unique=True,
        verbose_name='Заголовок',
    )
    description = models.TextField(
        verbose_name='Описание'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Ad(AbstractModel):
    """Модель объявления."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='ads'
    )
    image_url = models.ImageField(
        upload_to='ad_images',
        verbose_name='Изображение',
        default='',
        **constants.NULLABLE,
        validators=[
            FileExtensionValidator(
                allowed_extensions=constants.IMAGE_EXTENSIONS
            )
        ],
    )
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория ',
        related_name='categories',
        on_delete=models.PROTECT
    )
    condition = models.CharField(
        max_length=constants.MAX_CHOICES_LENGTH,
        choices=chcs.AD_CONDITION_CHOICES,
        default=chcs.AdCondition.NEW,
        verbose_name="Состояния товара"
    )
    created_at = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return f'Товар: {self.title}, категория: {self.category.title}'


class Category(AbstractModel):
    """Модель категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ExchangeProposal(models.Model):
    """Модель предложения обмена."""

    ad_sender = models.ForeignKey(
        Ad,
        verbose_name='Объявление отправителя',
        on_delete=models.CASCADE,
        related_name='sender_ads'
    )
    ad_receiver = models.ForeignKey(
        Ad,
        verbose_name='Объявление получателя',
        on_delete=models.CASCADE,
        related_name='receiver_ads'
    )
    comment = models.TextField(
        **constants.NULLABLE,
        verbose_name='Комментарий'
    )
    status = models.CharField(
        max_length=constants.MAX_CHOICES_LENGTH,
        choices=chcs.PROPOSAL_STATUS_CHOICES,
        default=chcs.Status.PENDING,
        verbose_name="Статус предложения"
    )
    created_at = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
        constraints = [
            models.UniqueConstraint(
                fields=['ad_sender', 'ad_receiver'],
                name='unique_ad_sender_ad_receiver'),
        ]

    def __str__(self):
        return (f'Объявление отправителя: {self.ad_sender.title},'
                f'объявление получателя: {self.ad_receiver.title}')


@receiver(post_delete, sender=Ad)
def delete_ad_image_file(sender, instance, **kwargs):
    """Удаляет изображения объявления из медиа-папки."""

    if instance.image_url:
        instance.image_url.delete(save=False)


@receiver(pre_save, sender=Ad)
def delete_old_image_on_change(sender, instance, **kwargs):
    """Удаляет старое изображение при замене нового."""

    if not instance.pk:
        return

    try:
        old_instance = Ad.objects.get(pk=instance.pk)
    except Ad.DoesNotExist:
        return

    old_image = old_instance.image_url
    new_image = instance.image_url

    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            old_image.delete(save=False)
