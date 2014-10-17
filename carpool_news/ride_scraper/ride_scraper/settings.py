# -*- coding: utf-8 -*-

# Scrapy settings for ride_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'ride_scraper'

SPIDER_MODULES = ['ride_scraper.spiders']
NEWSPIDER_MODULE = 'ride_scraper.spiders'

ITEM_PIPELINES = {
    'ride_scraper.pipelines.RideSavingPipeline': 1,
    'ride_scraper.pipelines.SetSourcePipeline': 2,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'ride_scraper (+http://www.yourdomain.com)'

# Import django models
import sys
import os

# Django project path, relative to the scrapy app
current_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
django_project_dir = os.path.join(current_dir, '../')
sys.path.append(django_project_dir)

# Django settings and startup
os.environ['DJANGO_SETTINGS_MODULE'] = 'carpool_news.settings'

import django
django.setup()
