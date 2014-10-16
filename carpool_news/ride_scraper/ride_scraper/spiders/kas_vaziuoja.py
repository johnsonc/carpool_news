# -*- coding: utf8 -*-
import re
import arrow    # datetime parsing
from urlparse import urljoin
from scrapy.spider import BaseSpider
from scrapy.http import Request
from ride_scraper.items import RideItem


class KasVaziuojaSpider(BaseSpider):
    name = 'kas_vaziuoja'
    start_urls = ['http://www.kasvaziuoja.lt/']

    # Crawler entry point
    def parse(self, response):
        rides = response.xpath("//div[@class='entry black']")
        for ride in rides:
            # Actual ad link
            ride_url = ride.xpath(
                "div[@class='photoBox']/a/@href").extract()[0]
            ride_url = urljoin(response.url, ride_url)
            ride_item = RideItem()

            # Check if ride is being offered or looked for
            is_looking_for = ride.xpath(
                "div[@class='message']/div/strong/span/text()").extract()[0]

            if is_looking_for == u'Ieškau':
                ride_item['is_looking_for'] = True
            elif is_looking_for == u'Siūlau':
                ride_item['is_looking_for'] = False

            yield Request(
                url=ride_url,
                meta={'ride_item': ride_item},
                callback=self.parse_ride)

    def parse_ride(self, response):
        ride_item = response.meta['ride_item']

        # Parse main fields
        fields = response.xpath(
            "//div[@class='fl info']/strong/following-sibling::text()").extract()
        last = len(fields) - 1
        ride_item['phone'] = fields[last - 2].strip()
        ride_item['ride_date'] = arrow.get(fields[last - 1].strip())
        ride_item['content'] = fields[last].strip()
        ride_item['site_url'] = response.url

        # Parse cities
        route_raw = response.xpath(
            # 'ė' left out intentionally to avoid encoding problems
            "//h1[contains(text(), 'Kelion')]/a/text()").extract()[0]
        cities = route_raw.split("-")
        ride_item['routes'] = [{
            'origin': cities[0].strip(),
            'destination': cities[1].strip()
        }]

        # Parse facebook url
        # Instead of trying to click javascript link in the ad content,
        # use <script> tags containing the actual FB url.
        fb_link_js = response.xpath(
            "//script[contains(text(), 'facebook.com')]/text()").extract()[0]
        fb_idx = fb_link_js.index('facebook.com')
        # Extract what's between apostrophes - full url
        fb_url_start = fb_link_js.rfind("'", 0, fb_idx) + 1
        fb_url_end = fb_link_js.find("'", fb_idx)
        fb_url = fb_link_js[fb_url_start:fb_url_end]
        ride_item['fb_url'] = fb_url

        yield ride_item

    def _parse_is_looking_for(self, html):
        pass
