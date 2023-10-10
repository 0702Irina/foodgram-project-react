import csv

from recipes.models import Ingredient

with open('/app/data/ingredients.csv', encoding='utf-8', mode='r') as file: 
    csv_reader = csv.DictReader(file) 
    for row in csv_reader: 
        Ingredient.objects.get_or_create()