# Generated by Django 5.0.6 on 2024-07-17 17:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chatrooms_name_alter_messages_chatroom'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatrooms',
            name='members',
            field=models.ManyToManyField(related_name='member_of', to=settings.AUTH_USER_MODEL),
        ),
    ]