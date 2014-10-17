# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0003_auto_20141017_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('ad_id_pattern', models.CharField(max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='ride',
            old_name='site_url',
            new_name='ad_url',
        ),
        migrations.AddField(
            model_name='ride',
            name='ad_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ride',
            name='ad_source',
            field=models.ForeignKey(to='rides.AdSource', null=True),
            preserve_default=True,
        ),
    ]
