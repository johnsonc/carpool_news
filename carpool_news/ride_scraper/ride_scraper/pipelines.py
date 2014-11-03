# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from django.core.exceptions import ObjectDoesNotExist
from rides.models import Route, Location, AdSource


class RideSavingPipeline(object):
    def process_item(self, item, spider):
        # Process raw origin/destination pairs
        try:
            for route_dict in item['routes']:
                origin, created = Location.objects.get_or_create(
                    name=route_dict['origin'])
                destination, created = Location.objects.get_or_create(
                    name=route_dict['destination'])
                route, created = Route.objects.get_or_create(
                    origin=origin,
                    destination=destination)
                # Ride needs a PK value before using many-to-many relationship
                item.save()
                item.instance.routes.add(route)
                item.save()
                return item
        except:
            if item.instance.pk:
                # Anything wrong happened after item was saved?
                item.instance.delete()
            # Rethrow
            raise


class SetSourcePipeline(object):
    def process_item(self, item, spider):
        # Get ad source from DB or create new if needed
        try:
            source = AdSource.objects.get(name=spider.name)
        except:
            source = AdSource.objects.create(
                name=spider.name,
                # CAUTION - what if there are multiple urls???
                url=spider.start_urls[0],
                ad_id_pattern=spider.ad_id_pattern)
        item.instance.ad_source = source
        item.save()
        return item
