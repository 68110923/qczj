# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join
from qczjbm.items import DfvideoItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
from os import path
import os


class DfvideospiderSpider(CrawlSpider):
    name = 'DfVideoSpider'
    allowed_domains = ['2263mk.com', 'busdlweb.com']
    start_urls = ['https://www.2263mk.com/']

    rules = (
        Rule(LinkExtractor(allow=r'正则表达式'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = DfvideoItem()
        try:
            item["video_url"] = response.xpath('//input[@id="mp4Source"]/@value').extract()[0]
            item["video_title"] = response.xpath('//meta[@name="description"]/@content').extract()[0]
            # print(item)
            item["video_url"] = 'http:' + item['video_url']
            yield scrapy.Request(url=item['video_url'], meta=item, callback=self.parse_video)
        except:
            pass

    def parse_video(self, response):

        i = response.meta
        file_name = Join()([i['video_title'], '.mp4'])
        base_dir = path.join(path.curdir, 'VideoDownload')
        video_local_path = path.join(base_dir, file_name.replace('?', ''))
        i['video_local_path'] = video_local_path

        if not os.path.exists(base_dir):
            os.mkdir(base_dir)

        with open(video_local_path, "wb") as f:
            f.write(response.body)

        yield i
