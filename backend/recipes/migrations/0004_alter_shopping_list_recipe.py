# Generated by Django 3.2 on 2023-10-08 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping_list',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sllist_recipes', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]
