# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.files import FilesPipeline
from qczjbm.settings import IMAGES_STORE, FILES_STORE
import os
import pymysql


class QczjbmPipeline:
    def process_item(self, item, spider):
        return item


class QczjbmImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(QczjbmImagePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(QczjbmImagePipeline, self).file_path(request, response, info)
        title = request.item.get('title')
        arctic = request.item.get('arctic')
        image_store = IMAGES_STORE
        category_path1 = os.path.join(image_store, arctic)
        if not os.path.exists(category_path1):
            os.mkdir(category_path1)
        category_path = os.path.join(category_path1, title)
        if not os.path.exists(category_path):
            os.mkdir(category_path)
        image_name = path.replace('full/', '')
        image_path = os.path.join(category_path, image_name)
        return image_path


class PornographicPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': '000578',
            'database': 'blog',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        _sql = 'insert into pornographic(files,file_urls,videoName,atUrl) values (%s,%s,%s,%s)'
        print(item['videoName'], item['atUrl'])
        self.cursor.execute(_sql, (item['files'], item['file_urls'][0], item['videoName'], item['atUrl']))
        self.conn.commit()
        return item
    def on_close(self):
        self.cursor.close()
        self.conn.close()


# 下视频
class PornographicFilesPipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(PornographicFilesPipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        videoName = request.item.get('videoName')
        file_store = FILES_STORE
        image_path = os.path.join(file_store, videoName, '.mp4')
        return image_path

class doubantop250Pipeline(object):
    def __init__(self):
        import csv
        self.f=open('./豆瓣top250.csv', 'w', encoding='utf-8',newline='')
        self.csv_writer = csv.writer(self.f)
        self.csv_writer.writerow(["电影名称", "导演主演", "评分", "评价人数", "介绍", "具体链接"])
    def process_item(self, item, spider):
        self.csv_writer.writerow([item['filmTitle'],item['synopsis'],item['graded'],item['gradedNum'],item['introduce'],item['url']])

    def on_close(self):
        self.f.close()