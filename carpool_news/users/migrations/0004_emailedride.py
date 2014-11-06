# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import arrow_field.model_fields


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0008_auto_20141105_1823'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_auto_20141104_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailedRide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email_date', arrow_field.model_fields.ArrowField()),
                ('ride', models.ForeignKey(related_name=b'emailed_users', to='rides.Route')),
                ('user', models.ForeignKey(related_name=b'emailed_rides', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
