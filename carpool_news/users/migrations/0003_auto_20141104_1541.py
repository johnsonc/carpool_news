# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20141030_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userroute',
            name='is_looking_for',
            field=models.BooleanField(default=False, choices=[(False, b'Si\xc5\xablo'), (True, b'Ie\xc5\xa1ko')]),
        ),
    ]
