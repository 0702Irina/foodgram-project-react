from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from colorfield.fields import ColorField

from recipes.constants import (
    COLOR_PALETTE,
    MIN_AMOUNT,
    MAX_AMOUNT,
    MIN_TIME,
    MAX_TIME
)


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        unique=True,
        blank=True,
        max_length=200,
        help_text='Укажите логин',
    )
    password = models.CharField(
        'Пароль',
        max_length=200,
        help_text='Укажите пароль',

    )
    first_name = models.CharField(
        'Имя',
        blank=True,
        max_length=200,
        help_text='Укажите имя',
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        max_length=200,
        help_text='Укажите фамилию',

    )
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=200,
        help_text='Укажите email',
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:20]


class Ingredient(models. Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Укажите название ингредиента',
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=200,
        help_text='Выберите единицу измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name[:20]


class Tag(models. Model):
    name = models.CharField(
        'Название',
        unique=True,
        max_length=200,
        help_text='Укажите название'
    )
    color = ColorField(
        'Цвет',
        default='#FF0000',
        format='hexa',
        samples=COLOR_PALETTE,
        help_text='Выберите цвет, нажмите на цветной квадрат'
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=200,
        help_text='Укажите слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:20]


class Follow(models. Model):
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        help_text='Укажите подписчика',
    )
    author = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите на кого подписывается пользователь',
    )

    class Meta:
        ordering = ('-user', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return f'{self.user} follows {self.author}'


class Recipe(models.Model):
    name = models.CharField(
        'Название',
        max_length=200,
        help_text='Укажите название рецепта',

    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тег',
        help_text='Выберите тег',
    )
    text = models.TextField(
        verbose_name='Способ приготовления',
        help_text='Опишите способ приготовления блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        help_text='Выберите ингридиент',
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=True,
        validators=(
            MinValueValidator(MIN_TIME),
            MaxValueValidator(MAX_TIME)
        ),
        verbose_name='Время приготовления блюда',
        help_text='Введите время приготовления блюда ',
    )
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор рецепта',
        help_text='Выберите автора рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата публикации',
        help_text='Укажите дату публикации',
    )
    image = models.ImageField(
        upload_to='recipe',
        verbose_name='Фото блюда',
        help_text='Добавьте фото готового блюда',
    )
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:20]


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_recipes',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        help_text='Выберите ингредиент',
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        ),
        verbose_name='Количество',
        help_text='Введите количество ингедиента',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Favorite(models. Model):
    user = models.ForeignKey(
        User,
        related_name='favorites',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'


class Shopping_list(models. Model):
    user = models.ForeignKey(
        User,
        related_name='sllists',
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='sllists',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
