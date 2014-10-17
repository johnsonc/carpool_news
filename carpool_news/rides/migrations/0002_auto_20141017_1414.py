# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import arrow_field.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='creation_time',
            field=arrow_field.model_fields.ArrowField(),
        ),
        migrations.AlterField(
            model_name='ride',
            name='ride_date',
            field=arrow_field.model_fields.ArrowField(),
        ),
    ]
