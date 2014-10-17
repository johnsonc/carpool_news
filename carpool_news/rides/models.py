from django.db import models
from arrow_field.model_fields import ArrowField


class Route(models.Model):
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)


class Ride(models.Model):
    # Advertisement creation date and time
    creation_time = ArrowField(null=True)

    # Expected date of the trip
    ride_date = ArrowField(null=True)

    # Raw advertisement text
    content = models.CharField(max_length=4000, null=True)

    # Boolean flag indicating if author is looking for a ride
    # instead of offering one
    is_looking_for = models.BooleanField(default=False)

    # Link to author's facebook profile
    fb_url = models.CharField(max_length=255, null=True)

    # Link to original ad
    site_url = models.CharField(max_length=255, null=True)

    # Author's contact phone number
    phone = models.CharField(max_length=30, null=True)

    # Origin and destination cities of this ride
    routes = models.ManyToManyField(Route)
