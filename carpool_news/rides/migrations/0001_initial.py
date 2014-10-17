# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_time', models.DateTimeField()),
                ('ride_date', models.DateField()),
                ('content', models.CharField(max_length=4000)),
                ('is_looking_for', models.BooleanField(default=False)),
                ('fb_url', models.CharField(max_length=255)),
                ('site_url', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin', models.CharField(max_length=255)),
                ('destination', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='ride',
            name='routes',
            field=models.ManyToManyField(to='rides.Route'),
            preserve_default=True,
        ),
    ]
