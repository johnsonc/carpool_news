# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.djangoitem import DjangoItem
from rides.models import Ride


# Map with existing django models
class RideItem(DjangoItem):
    django_model = Ride
    # Deal with ride/route mapping separately in pipelines.py
    routes = scrapy.Field()
