# -*- coding: utf-8 -*-
import scrapy
import re

from qczjbm.items import DouBanTop250


class Doubantop250Spider(scrapy.Spider):
    name = 'doubantop250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        resls = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for res_one in resls:
            filmTitle=''.join(res_one.xpath('.//div/div[2]/div[1]/a/span[1]/text()').get().split()) or ''
            synopsis=re.sub('[a-zA-Z0-9\./]','',''.join(res_one.xpath('.//div/div[2]/div[2]/p[1]/text()').get().split())) or ''
            graded=''.join(res_one.xpath('.//div/div[2]/div[2]/div/span[2]/text()').get()) or ''
            gradedNum=''.join(res_one.xpath('.//div/div[2]/div[2]/div/span[4]/text()').get()) or ''
            introduce=res_one.xpath('.//div/div[2]/div[2]/p[2]/span/text()').get() or ''
            url=res_one.xpath('.//div/div[2]/div[1]/a/@href').get().replace('\n','') or ''
            yield DouBanTop250(filmTitle=filmTitle,synopsis=synopsis,graded=graded,gradedNum=gradedNum,introduce=introduce,url=url)
        yield scrapy.Request(response.urljoin(response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/a/@href').get()),callback=self.parse)




