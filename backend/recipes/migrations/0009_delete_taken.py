# Generated by Django 3.2.21 on 2023-09-13 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_taken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Taken',
        ),
    ]