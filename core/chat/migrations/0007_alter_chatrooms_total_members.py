# Generated by Django 5.0.6 on 2024-07-18 11:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_chatrooms_banned_member_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrooms',
            name='total_members',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(2)]),
        ),
    ]
