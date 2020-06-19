# -*- coding: utf-8 -*-
import scrapy
from qczjbm.items import QczjbmItem


class QczjbmappSpider(scrapy.Spider):
    name = 'qczjbmapp'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/45.html#pvareaid=3454438']

    def parse(self, response):
        for page in range(45, 550):
            yield scrapy.Request(f'https://car.autohome.com.cn/pic/series-t/{page}.html', callback=self.extractContent)

    def extractContent(self, response):
        uiboxs = response.xpath('//div[@class="uibox"]')
        arctic = response.xpath('/html/body/div[2]/div/div[2]/div[7]/div/div[1]/h2/a/text()').get()
        for uibox in uiboxs:
            title = uibox.xpath('.//div[@class="uibox-title"]/a/text()').get()
            image_urls = uibox.xpath('.//div/ul/li/a/img/@src').getall()
            image_urls = list(map(lambda url: response.urljoin(url), image_urls))
            item = QczjbmItem(arctic=arctic,title=title, image_urls=image_urls)
            yield item
