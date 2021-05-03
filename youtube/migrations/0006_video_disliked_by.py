# Generated by Django 3.1.2 on 2021-04-26 10:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('youtube', '0005_auto_20210421_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='disliked_by',
            field=models.ManyToManyField(related_name='disliked_by', to=settings.AUTH_USER_MODEL),
        ),
    ]