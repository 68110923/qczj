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
    videoName = scrapy.Field()
    atUrl = scrapy.Field()
    pass


class DfvideoItem(scrapy.Item):
    video_url = scrapy.Field()  # 视频源url
    video_title = scrapy.Field()  # 视频标题
    video_local_path = scrapy.Field()  # 视频本地存储路径


class DouBanTop250(scrapy.Item):
    filmTitle = scrapy.Field()
    synopsis = scrapy.Field()
    graded = scrapy.Field()
    gradedNum = scrapy.Field()
    introduce = scrapy.Field()
    url = scrapy.Field()


class zhiyuan_Item(scrapy.Item):
    city = scrapy.Field()
    lot = scrapy.Field()
    lot_time = scrapy.Field()


class ZhiyuanBiaoItme(scrapy.Item):
    zhuanye_bag_class = scrapy.Field()
    zhuanye_class = scrapy.Field()
    zhuanye_zhuanye = scrapy.Field()


class zhiyuanxian_Item(scrapy.Item):
    city = scrapy.Field()
    school = scrapy.Field()
    specialty = scrapy.Field()
    fractional_line = scrapy.Field()


class ZhiyuanGaodifenItem(scrapy.Item):
    school_name = scrapy.Field()
    major_name = scrapy.Field()
    admissions_address = scrapy.Field()
    examinee_class = scrapy.Field()
    admission_to_the_batch = scrapy.Field()
    average_score = scrapy.Field()
    lowest_mark = scrapy.Field()
    nianfen = scrapy.Field()
    city = scrapy.Field()
    banxueleixing = scrapy.Field()
    zhuanyemenlei = scrapy.Field()
