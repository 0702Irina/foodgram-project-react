# Generated by Django 3.2 on 2023-09-19 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_recipeingredient_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='measurement_unit',
        ),
    ]
