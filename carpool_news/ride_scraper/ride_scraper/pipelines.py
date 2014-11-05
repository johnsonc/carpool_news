# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from rides.models import Ride, Route, Location, AdSource


def get_or_create_source(spider):
    source, created = AdSource.objects.get_or_create(
        name=spider.name,
        # CAUTION - what if there are multiple urls???
        url=spider.start_urls[0],
        ad_id_pattern=spider.ad_id_pattern)
    return source


class CheckExpiredPipeline(object):
    def process_item(self, item, spider):
        """
        Save original ad url of each scraped item
        """
        # Initialize the list here instead of 'open_spider' callback
        # as at that moment spider state is not available yet
        if 'scraped_items' not in spider.state:
            spider.state['scraped_items'] = []
        spider.state['scraped_items'].append(item)
        return item

    def close_spider(self, spider):
        """
        Mark expired ads of particular ad source (spider).
        """
        source = get_or_create_source(spider)
        db_items = source.rides.filter(
            is_expired=False)
        for db_item in db_items:
            # Method of determining whether ad is expired depends on the source
            # so should be described in each spider
            if spider.is_expired(db_item, spider.state['scraped_items']):
                db_item.is_expired = True
                db_item.save()


class CheckExistingPipeline(object):
    def process_item(self, item, spider):
        """
        Check if ad does not yet exist in DB by using ad_url.
        """
        try:
            Ride.objects.get(ad_url=item['ad_url'])
            # If already exists:
            raise DropItem("Ride ad already exists: %s" % item['ad_url'])
        except Ride.DoesNotExist:
            # Continue processing this item
            return item


class RideSavingPipeline(object):
    def process_item(self, item, spider):
        """
        Save scraped ad.
        """
        try:
            # Ride needs a PK value before using many-to-many relationship
            item.save()
            # Process raw origin/destination pairs
            for route_dict in item['routes']:
                origin, created = Location.objects.get_or_create(
                    name=route_dict['origin'])
                destination, created = Location.objects.get_or_create(
                    name=route_dict['destination'])
                route, created = Route.objects.get_or_create(
                    origin=origin,
                    destination=destination)
                item.instance.routes.add(route)

            # Set source from which the ad was scraped.
            item.instance.ad_source = get_or_create_source(spider)

            # Done!
            item.save()
            return item
        except:
            if item.instance.pk:
                # Anything wrong happened after item was saved?
                item.instance.delete()
            # Rethrow (and drop this item)
            raise
