import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Добавляет ingredients.csv в БД'

    def handle(self, *args, **options):
        with open(
            '/home/stas/Dev/foodgram-project-react/data/ingredients.csv'
        ) as f:
            reader = csv.reader(f, delimiter=',')
            next(reader, None)
            for row in reader:
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
