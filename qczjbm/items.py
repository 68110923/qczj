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


class DfvideoItem(scrapy.Item):
    video_url = scrapy.Field()#视频源url
    video_title = scrapy.Field()#视频标题
    video_local_path = scrapy.Field()#视频本地存储路径