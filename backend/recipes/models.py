from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Shopping_list(models. Model):
    pass


class Favorites(models. Model):
    pass


class Ingredient(models. Model):
    pass


class Tag(models. Model):
    pass


class Follow(models. Model):
    pass


class Recipe(models.Model):
    '''Модель создания постов пользователей.'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор статьи',
        help_text='Укажите автора статьи',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Введите описание рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Укажите дату публикации',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Название ингридиента',
        help_text='Выберите название ингридиента из списка',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text[:10]