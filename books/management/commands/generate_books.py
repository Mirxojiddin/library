import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Category, SubCategory, Book


class Command(BaseCommand):
    help = 'Generate 100 random books'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Categories and SubCategories
        categories = Category.objects.all()
        subcategories = [SubCategory.objects.create(category=random.choice(categories), name=fake.word()) for _ in range(30)]

        # Create 100 books
        for _ in range(100):
            category = random.choice(categories)
            sub_category = random.choice(subcategories)
            Book.objects.create(
                title=fake.sentence(nb_words=4),
                description=fake.text(),
                author=fake.name(),
                year=fake.year(),
                pages=random.randint(100, 1000),
                category=category,
                sub_category=sub_category,
                url=fake.url(),
                file=None,  # Assuming you handle file uploads separately
                size=random.randint(1, 1000),
                isbn=fake.isbn13()
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated 100 books'))
