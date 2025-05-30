# Generated by Django 5.1.1 on 2025-05-26 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ads', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='ad',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='ads.category', verbose_name='Категория '),
        ),
        migrations.AddField(
            model_name='exchangeproposal',
            name='ad_receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver_ads', to='ads.ad', verbose_name='Объявление получателя'),
        ),
        migrations.AddField(
            model_name='exchangeproposal',
            name='ad_sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_ads', to='ads.ad', verbose_name='Объявление отправителя'),
        ),
        migrations.AddConstraint(
            model_name='exchangeproposal',
            constraint=models.UniqueConstraint(fields=('ad_sender', 'ad_receiver'), name='unique_ad_sender_ad_receiver'),
        ),
    ]
