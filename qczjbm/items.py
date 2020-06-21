# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QczjbmItem(scrapy.Item):
    title = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    arctic = scrapy.Field()
    pass

class PornographicItem(scrapy.Item):
    files = scrapy.Field()
    file_urls = scrapy.Field()
    videoName=scrapy.Field()
    atUrl = scrapy.Field()
    pass