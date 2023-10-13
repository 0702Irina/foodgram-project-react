# Generated by Django 3.2 on 2023-10-13 06:54

from django.db import migrations, models
import django.db.models.deletion
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20231013_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(help_text='Выберите ингридиент', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(help_text='Выберите ингредиент', on_delete=django.db.models.deletion.CASCADE, to='recipes.ingredient', validators=[recipes.validators.validate_ingredients], verbose_name='Ингредиент'),
        ),
    ]
