from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создает суперпользователя (админа), если он ещё не существует."""

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@email.com'
        password = 'admin'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" уже существует.'))
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" успешно создан.'))
