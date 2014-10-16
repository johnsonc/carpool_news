# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KasVezaItem(scrapy.Item):
    # Advertisement creation datetime
    creation_time = scrapy.Field()

    # Raw advertisement text
    content = scrapy.Field()

    # Boolean flag indicating if author is looking for a ride
    # instead of offering one
    is_looking_for = scrapy.Field()

    # Link to author's facebook profile
    fb_url = scrapy.Field()

    # Link to original ad
    site_url = scrapy.Field()

    # Author's contact phone number
    phone = scrapy.Field()

    # Origin and destination cities of this ride
    routes = scrapy.Field()
