from django.contrib import admin

from recipes.models import (
    RecipeIngredient,
    Shopping_list,
    Ingredient,
    Favorites,
    # Follow,
    Recipe,
    Tag,
    User
)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'image',
        'text',
        'pub_date',
        'author'
    )
    search_fields = ('name', 'ingredient', 'tag')
    list_filter = ('pub_date', 'author', 'tag', 'ingredient')
    empty_value_display = '-пусто-'
    verbose_name = 'Рецепты',
    inlines = (RecipeIngredientInline, )


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'unit'
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    verbose_name = 'Ингридиент',


@admin.register(Shopping_list)
class Shopping_listAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
        'name'
    )
    search_fields = ('user',)
    list_filter = ('user',)
    empty_value_display = '-пусто-'
    verbose_name = 'Список покупок',


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
        'color',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'
    verbose_name = 'Тег',


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name',
        'recipe'
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email'
    )
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
    verbose_name = 'Пользователь',
