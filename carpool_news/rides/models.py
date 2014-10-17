import re
from django.db import models
from arrow_field.model_fields import ArrowField


class AdSource(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    ad_id_pattern = models.CharField(max_length=255, null=True)


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
            self.ad_id = parsed_ad_id(
                self.ad_url,
                self.ad_source.ad_id_pattern)
        super(Ride, self).save()


def parsed_ad_id(url, pattern):
    match = re.search(pattern, url)
    if match:
        # Assuming that pattern contains one named group (i.e. 'id')
        return int(match.groupdict().values()[0])
    else:
        return None


def max_scraped_id(source_name):
    """Latest scraped ad ID from given source
    """
    return Ride.objects\
        .filter(ad_source__name=source_name)\
        .aggregate(models.Max('ad_id'))['ad_id__max']
