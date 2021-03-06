# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-02 05:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('videoapp', '0002_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribed_to', models.ForeignKey(on_delete=models.SET(main.models.get_ghost_user), related_name='subscribed_to', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=models.SET(main.models.get_ghost_user), related_name='subscribed_from', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
