# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def populate_locations(apps, schema_editor):
    """
    Collect unique city names from Route table
    and populate the new Location table
    """
    # Initialize models
    Route = apps.get_model('rides', 'Route')
    Location = apps.get_model('rides', 'Location')

    # Get existing city names
    unique_locations = sorted(list(set([
        city
        for pair in [
            [route.origin, route.destination]
            for route in Route.objects.all()
        ]
        for city in pair
    ])))

    # Create new Location instances
    for location in unique_locations:
        new_location = Location(name=location)
        new_location.save()


def map_locations_to_routes(apps, schema_editor):
    """
    Set 'origin' and 'destination' foreign keys
    by looking up with 'origin_old' and 'destination_old' location names
    in Route table.
    """
    Route = apps.get_model('rides', 'Route')
    Location = apps.get_model('rides', 'Location')
    all_locations = Location.objects.all()
    # Do the mapping
    for route in Route.objects.all():
        location_origin = next(
            location for location in all_locations
            if location.name == route.origin_old)
        location_destination = next(
            location for location in all_locations
            if location.name == route.destination_old)
        route.origin = location_origin
        route.destination = location_destination
        route.save()


def map_locations_to_routes_reverse(apps, schema_editor):
    """
    Set 'origin_old' and 'destination_old' location names
    by looking up locations via 'origin' and 'destination'
    foreign keys in Route table.
    """
    Route = apps.get_model('rides', 'Route')
    # Mapping
    for route in Route.objects.all():
        route.origin_old = route.origin.name
        route.destination_old = route.destination.name
        route.save()


class Migration(migrations.Migration):

    dependencies = [
        ('rides', '0004_auto_20141017_1736'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        # Collect unique city names from existing Route table
        # and fill the new table with this data
        migrations.RunPython(populate_locations),

        # Rename existing 'origin' and 'destination' columns
        migrations.RenameField(
            model_name='route',
            old_name='origin',
            new_name='origin_old'),
        migrations.RenameField(
            model_name='route',
            old_name='destination',
            new_name='destination_old'),

        # Create new foreign keys with the same names
        migrations.AddField(
            model_name='route',
            name='destination',
            field=models.ForeignKey(
                related_name=b'destinations',
                to='rides.Location',
                null=True),
        ),
        migrations.AddField(
            model_name='route',
            name='origin',
            field=models.ForeignKey(
                related_name=b'origins',
                to='rides.Location',
                null=True),
        ),

        # Do the actual mapping between Location and Route tables
        migrations.RunPython(
            map_locations_to_routes,
            reverse_code=map_locations_to_routes_reverse),

        # Add NOT NULL constraints on new foreign keys
        migrations.AlterField(
            model_name='route',
            name='destination',
            field=models.ForeignKey(
                related_name=b'destinations',
                to='rides.Location',
                null=False),
        ),
        migrations.AlterField(
            model_name='route',
            name='origin',
            field=models.ForeignKey(
                related_name=b'origins',
                to='rides.Location',
                null=False),
        ),

        # Drop the old columns
        migrations.RemoveField(
            model_name='route',
            name='origin_old'),
        migrations.RemoveField(
            model_name='route',
            name='destination_old'),
    ]
