# Generated by Django 3.2.21 on 2023-09-13 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20230913_0841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_subscriptions',
            new_name='subscriptions',
        ),
    ]