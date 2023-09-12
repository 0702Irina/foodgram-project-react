from django_filters.rest_framework import FilterSet
from django_filters.rest_framework.filters import CharFilter
from recipes.models import Ingredient


class IngredientFilter(FilterSet):
    name = CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ['name']