# -*- coding: utf-8 -*-
import scrapy
from qczjbm.items import zhiyuan_Item

class ZhiyuanSpider(scrapy.Spider):
    name = 'zhiyuan'
    allowed_domains = ['quark.sm.cn']
    # start_urls = ['http://quark.sm.cn/']
    start_urls = [f'https://quark.sm.cn/s?q={i}志愿填报查询&uc_param_str=dnntnwvepffrgibijbprsvdsdichmennut&from=kkframenew&by=submit&snum=6' for i in ["北京",
              "天津", "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江", "上海", "江苏", "浙江", "安徽", "福建", "江西", "山东", "河南", "湖北",
              "湖南", "广东", "广西", "海南", "重庆", "四川", "贵州", "云南", "西藏", "陕西", "甘肃", "青海", "宁夏", "新疆"
              ]]
    def parse(self, response):
        city = response.xpath('//*[@id="sc_gaokao_programme_1_1"]/div/div[1]/div/div/div/form/span/text()').get()
        for i in response.xpath(
                '//*[@id="sc_gaokao_programme_1_1"]/div/div[2]/div/div[2]/div[3]/div/div[1]/table/tbody/tr'):
            lot = i.xpath('./td[1]//span/text()').get()
            lot_time = i.xpath('./td[2]//span/text()').get()
            yield zhiyuan_Item(city=city,lot=lot, lot_time=lot_time)