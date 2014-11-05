# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0006_auto_20141104_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ride',
            name='is_processed',
        ),
        migrations.AlterField(
            model_name='ride',
            name='ad_source',
            field=models.ForeignKey(related_name=b'rides', to='rides.AdSource', null=True),
        ),
    ]
