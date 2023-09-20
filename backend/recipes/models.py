from django.contrib.auth.models import AbstractUser
from django.db import models
from colorfield.fields import ColorField


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        unique=True,
        blank=True,
        max_length=200,
    )
    password = models.CharField(
        'Пароль',
        max_length=200,

    )
    first_name = models.CharField(
        'Имя',
        blank=True,
        max_length=200,
    )
    last_name = models.CharField(
        'Фамилия',
        blank=True,
        max_length=200,

    )
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=200,
    )
    is_subscriptions = models.BooleanField(default=False, blank=True,)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username[:20]


class Ingredient(models. Model):
    name = models.CharField(
        'Ингридиент',
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name[:20]


class Tag(models. Model):
    name = models.CharField(
        'Тег',
        unique=True,
        max_length=200,
    )
    color = ColorField(
        default='#FF0000',
        format="hexa"
    )
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=200,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name[:20]


class Follow(models. Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        help_text='Укажите подписчика',
    )
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите на кого подписываемся',
    )

    class Meta:
        ordering = ('-user', )
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                name='unique_follow',
                fields=('user', 'following')
            ),
        )

    def __str__(self) -> str:
        return f'{self.user} follows {self.following}'


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
    )
    text = models.TextField(
        verbose_name='Способ приготовления',
        help_text='Опишите способ приготовления блюда',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Название ингридиента',
        help_text='Выберите название ингридиента из списка',
    )
    cooking_time = models.PositiveIntegerField(
        null=True,
        verbose_name='Время приготовления блюда',
        help_text='Введите время приготовления блюда ',
    )
    author = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата публикации',
        help_text='Укажите дату публикации',
    )
    image = models.ImageField(
        upload_to='recipe/%Y/%m/%d/',
        null=True,
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
        related_name='recipengredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'


class Shopping_list(models. Model):
    name = models.CharField(
        verbose_name='Список покупок',
        max_length=200
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
    )
    user = models.ForeignKey(
        User,
        related_name='sl',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorites(models. Model):
    name = models.CharField(
        verbose_name='Избранные рецепты',
        max_length=200
    )
    user = models.ForeignKey(
        User,
        related_name='faworites',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
