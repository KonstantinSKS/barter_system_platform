from django.core.management import BaseCommand
from ads.models import Category


class Command(BaseCommand):
    """Создает тестовые категории, если они ещё не существуют."""

    categories_data = [
        {"title": "Книги", "description": "Художественные книги"},
        {"title": "Смартфоны", "description": "Android и Ios"},
        {"title": "Садовый инвентарь", "description": "Газонокосилки и лопаты"},
    ]

    def handle(self, *args, **options):
        for data in self.categories_data:
            self._create_category(data["title"], data["description"])

    def _create_category(self, title: str, description: str):
        if Category.objects.filter(title=title).exists():
            self.stdout.write(self.style.WARNING(f'Категория "{title}" уже существует.'))
        else:
            Category.objects.create(title=title, description=description)
            self.stdout.write(self.style.SUCCESS(f'Категория "{title}" успешно создана.'))
