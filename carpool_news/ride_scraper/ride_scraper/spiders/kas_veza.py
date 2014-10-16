# -*- coding: utf8 -*-
import re
from urlparse import urljoin
from dateutil.parser import parse
from scrapy.spider import BaseSpider
from scrapy.http import Request
from ride_scraper.items import RideItem


class KasVezaSpider(BaseSpider):
    name = "kas_veza"
    start_urls = ["https://www.kasveza.lt/marsrutai/"]

    def __init__(self, last_scraped_id=None, *args, **kwargs):
        super(KasVezaSpider, self).__init__(*args, **kwargs)
        # Limit scraping to these ads which have ID higher than
        # this parameter.
        if last_scraped_id:
            self.last_scraped_id = int(last_scraped_id)
        else:
            self.last_scraped_id = 0
        self.id_pattern = re.compile('skelbimas/(?P<id>\d+)')

    # Crawler entry point
    def parse(self, response):
        # Table rows representing different routes
        routes = response.xpath("//tr[@class='rowlink']")

        # for route in routes[:5]:
        for route in routes:
            # Extract relative path to this route
            route_url = route.xpath(".//a/@href").extract()[0]
            # Make an absolute url
            route_url = urljoin(response.url, route_url)

            # And crawl into it
            yield Request(
                url=route_url,
                callback=self.parse_route)

    def parse_route(self, response):
        # Paginated list of rides for selected route
        # Need to handle the pages first.
        pages = response.xpath("//ul[@class='pagination']/li/a/@href").extract()
        for page in pages:
            page_url = urljoin(response.url, page)
            yield Request(
                url=page_url,
                callback=self.parse_route_page)

    def parse_route_page(self, response):
        # Newest available rides of this route - one page
        rides = response.xpath("//tr[@class='rowlink']")
        for ride in rides:
            # Specific ride: next url to be crawled
            ride_url = ride.xpath(".//a/@href").extract()[0]
            ride_url = urljoin(response.url, ride_url)

            # Check if this ad is new and not yet scraped
            id = self._get_id_from_url(ride_url)
            if id > self.last_scraped_id:
                ride_item = RideItem()
                # Advertisement creation datetime
                creation_time_str = ride.xpath(".//a/text()").extract()[0]
                creation_time_date = parse(creation_time_str)
                ride_item['creation_time'] = creation_time_date

                # Check if ride is being offered or looked for
                img_src = ride.xpath(".//img/@src").extract()[0]
                ride_item['is_looking_for'] = "nocar" in img_src

                yield Request(
                    url=ride_url,
                    meta={'ride_item': ride_item},
                    callback=self.parse_ride)

    def parse_ride(self, response):
        ride_item = response.meta['ride_item']
        # Author's facebook profile
        fb_url = response.xpath(
            "//div[@class='media-body']/p/a/@href").extract()[0]
        fb_url = fb_url.replace("/redirect?url=", "")
        ride_item['fb_url'] = fb_url
        ride_item['site_url'] = response.url

        # Phone number (optional)
        phone = response.xpath(
            "//span[contains(@class, 'glyphicon-phone-alt')]/../text()") \
            .extract()
        if phone:
            ride_item['phone'] = phone[0].strip()

        # Advertisement text
        content = response.xpath(
            "//span[@class='hidden-xs']/text()").extract()[0]
        ride_item['content'] = content

        # Route list
        routes_raw = response.xpath(
            "//small[contains(text(), 'Priskirti')]/following-sibling::node()/li").extract()
        routes = []
        for route_raw in routes_raw:
            # Parse origin and destination city names
            cities = self._parse_route_li(route_raw)
            if cities:
                routes.append(cities)
        ride_item['routes'] = routes

        yield ride_item

    def _parse_route_li(self, html):
        """
        Finds span with bootstrap arrow icon and takes the names of cities
        going before and after that span.

        Expected html:
        <li>
            <a class="btn btn-default btn-xs" style="margin-bottom: 10px;" href="../../marsrutas/9/15/">
                Kaunas
                <span class="glyphicon glyphicon-arrow-right"></span>
                Kuršėnai
                <span class="glyphicon glyphicon-search"></span>
            </a>
        </li>
        """
        pattern = re.compile((
            '>(?P<origin>[^<]*)'
            '(<span class="glyphicon glyphicon-arrow-right"></span>)'
            '(?P<destination>[^<]*)'))
        match = re.search(pattern, html)
        if match:
            # Remove trailing white space
            return {
                'origin': match.groupdict()['origin'].strip(),
                'destination': match.groupdict()['destination'].strip()
            }
        else:
            return {}

    def _get_id_from_url(self, url):
        """
        Parse ID from ad url
        """
        match = re.search(self.id_pattern, url)
        if match:
            return int(match.groupdict()['id'])
        else:
            return None
