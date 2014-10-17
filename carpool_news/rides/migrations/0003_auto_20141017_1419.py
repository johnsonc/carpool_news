# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import arrow_field.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0002_auto_20141017_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='content',
            field=models.CharField(max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='creation_time',
            field=arrow_field.model_fields.ArrowField(null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='fb_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='phone',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='ride_date',
            field=arrow_field.model_fields.ArrowField(null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='site_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
