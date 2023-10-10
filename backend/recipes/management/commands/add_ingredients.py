import csv

from recipes.models import Ingredient

MODEL = Ingredient

csv_file_paths = '/data/ingredients.cvs'

with open(csv_file_paths, encoding='utf-8', mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        Ingredient.objects.get_or_create()