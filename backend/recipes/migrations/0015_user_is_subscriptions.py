# Generated by Django 3.2.21 on 2023-09-13 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_remove_user_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_subscriptions',
            field=models.BooleanField(default=False),
        ),
    ]
