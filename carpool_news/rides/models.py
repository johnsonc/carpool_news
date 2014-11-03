import re
from django.db import models
from django.contrib.auth.models import User
from arrow_field.model_fields import ArrowField


class AdSource(models.Model):
    # Shorthand name of ad source (i.e. 'kas_veza')
    name = models.CharField(max_length=255)

    # Initial URL of this source (i.e. 'www.kasveza.lt/marsrutai')
    url = models.CharField(max_length=255)

    # Regexp for parsing ad ID from its url
    ad_id_pattern = models.CharField(max_length=255, null=True)


class Location(models.Model):
    name = models.CharField(max_length=255)

    @staticmethod
    def get_by_name(name):
        try:
            return Location.objects.filter(name=name)[0]
        except:
            return None

    def __unicode__(self):
        return self.name


class Route(models.Model):
    # Place of departure
    origin = models.ForeignKey('Location', related_name='origins')

    # Place of arrival
    destination = models.ForeignKey('Location', related_name='destinations')

    # Users interested in (following) this route
    users = models.ManyToManyField(
        User,
        through='users.UserRoute',
        related_name='routes')


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
    ad_url = models.CharField(max_length=255, null=True)

    # Ad ID - calculated from site_url
    ad_id = models.IntegerField(null=True)

    # Site from which this ride was scraped
    ad_source = models.ForeignKey(AdSource, null=True)

    # Author's contact phone number
    phone = models.CharField(max_length=30, null=True)

    # Origin and destination cities of this ride
    routes = models.ManyToManyField(Route)

    def save(self):
        # Persist parsed ad ID and continue with usual saving
        if self.ad_url and self.ad_source:
            # Parse ad ID from url
            match = re.search(
                self.ad_source.ad_id_pattern,
                self.ad_url)
            if match:
                # Assuming that pattern contains one named group (i.e. 'id')
                self.ad_id = int(match.groupdict().values()[0])
        super(Ride, self).save()
