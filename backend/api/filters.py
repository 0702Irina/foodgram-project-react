from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    # is_farorited = filters.NumberFilter(
    #     method='filter_is_favorited'
    # )
    is_in_shopping_cart = filters.NumberFilter(
        method='filter_shoppingcart'
    )

    class Meta:
        model = Recipe
        fields = (
            # 'is_farorited',
            'is_in_shopping_cart',
            'author',
            'tags'
        )

    # def filter_is_favorited(self, queryset, name, value):
    #     if value and self.request.user.is_authenticated:
    #         return queryset.filter(favorites__user=self.request.user)
    #     return queryset

    def filter_shoppingcart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(sllists__user=self.request.user)
        return queryset
