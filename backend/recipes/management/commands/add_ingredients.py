import csv

from django.core.management import BaseCommand, CommandError

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Импорт ингредиентов из csv файла'

    def handle(self, *args, **kwargs):
        try:
            with open(
                './data/ingredients.csv', 'r', encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                Ingredient.objects.bulk_create(
                    Ingredient(**row) for row in reader
                )
            self.stdout.write(self.style.SUCCESS('Ингредиенты загружены'))
        except Exception as error:
            CommandError(str(error))