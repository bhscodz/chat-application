# Generated by Django 5.0.6 on 2024-07-18 06:43

import django.core.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_alter_chatrooms_admin'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatrooms',
            name='private',
        ),
        migrations.AddField(
            model_name='chatrooms',
            name='banned_member',
            field=models.ManyToManyField(blank=True, editable=False, null=True, related_name='banned_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='chatrooms',
            name='current_member',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='chatrooms',
            name='members',
            field=models.ManyToManyField(blank=True, editable=False, null=True, related_name='member_of', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='chatrooms',
            name='total_members',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
