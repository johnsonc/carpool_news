# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_emailedride'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailedride',
            name='ride',
            field=models.ForeignKey(related_name=b'emailed_users', to='rides.Ride'),
        ),
    ]
