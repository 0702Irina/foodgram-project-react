# Generated by Django 3.2 on 2023-10-08 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_shopping_list_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopping_list',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sllist', to='recipes.recipe', verbose_name='Рецепт'),
        ),
    ]