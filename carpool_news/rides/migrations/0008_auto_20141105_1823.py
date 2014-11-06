# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0007_auto_20141105_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='routes',
            field=models.ManyToManyField(related_name=b'rides', to=b'rides.Route'),
        ),
    ]
