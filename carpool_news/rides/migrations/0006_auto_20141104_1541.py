# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20141104_1541'),
        ('rides', '0005_auto_20141027_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='is_expired',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ride',
            name='is_processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='route',
            name='users',
            field=models.ManyToManyField(related_name=b'routes', through='users.UserRoute', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
