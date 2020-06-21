# -*- coding: utf-8 -*-
import scrapy
from qczjbm.items import PornographicItem


class PornographicSpider(scrapy.Spider):
    name = 'pornographic'
    allowed_domains = ['2263mk.com', 'busdlweb.com']
    start_urls = ['https://www.2263mk.com/move/3/','https://www.2263mk.com/move/1/','https://www.2263mk.com/move/7/']

    def parse(self, response):
        for pageUrl in response.selector.xpath('//select/option/@value').getall():
            # 每一页的页面
            yield scrapy.Request(response.urljoin(pageUrl), callback=self.pageDispose, dont_filter=True)

    def pageDispose(self, response):
        for pageVideoLinkUrl in response.xpath('//div[@class="box movie2_list"]/ul/li/a/@href').getall():
            # 每一个视频的页面
            yield scrapy.Request(response.urljoin(pageVideoLinkUrl), callback=self.video)

    def video(self, response):
        videoName = response.xpath('//strong/text()').get()
        videoUrl = response.xpath('/html/body/div[7]/div[4]/b/font/a/@href').get()
        files = response.xpath('/html/body/div[5]/div/span/a[3]/text()').get()
        atUrl = response.url
        item = PornographicItem(videoName=videoName, file_urls=[videoUrl, ], atUrl=atUrl,files=files)
        yield item
