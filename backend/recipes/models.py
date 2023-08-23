from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models. Model):
    name = models.CharField(
        'Ингридиент',
        max_length=200
    )
    unit = models.CharField(
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
        max_length=200
    )
    color = models.CharField(
        'Цвет',
        unique=True,
        max_length=15
    )
    slug = models.SlugField(
        'Слаг',
        unique=True,
        max_length=200
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
    following = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
        help_text='Укажите на кого подписываемся',
    )

    class Meta:
        ordering = ('-user',)
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

    def get_absolute_url(self):
        pass


class Recipe(models.Model):
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    text = models.TextField(
        verbose_name='Способ приготовления',
        help_text='Опишите способ приготовления блюда',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Название ингридиента',
        help_text='Выберите название ингридиента из списка',
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Тег',
        help_text='Выберите тег из списка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Укажите дату публикации',
    )
    image = models.ImageField(
        upload_to='recipe/%Y/%m/%d/',
        null=True,
        blank=True,
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

    def get_absolute_url(self):
        pass


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.IntegerField(
        'Количество',
    )


class Shopping_list(models. Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name='Список покупок',
        max_length=200
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def get_absolute_url(self):
        pass


class Favorites(models. Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    name = models.CharField(
        verbose_name='Избранное',
        max_length=200
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Избранный рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def get_absolute_url(self):
        pass
