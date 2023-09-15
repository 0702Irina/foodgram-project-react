# Generated by Django 3.2.21 on 2023-09-13 08:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='subscriptions',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]