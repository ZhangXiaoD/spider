#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-10 11:27:21
# Project: douban_music

from pyspider.libs.base_handler import *
import pymongo
import re


MONGO_host = '127.0.0.1'
MONGO_port = 27017
MONGO_db = 'pyspider'
MONGO_collection = 'douban_music'

class MongoDB(object):
    
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_host,MONGO_port)
        self.db = self.client[MONGO_db]
        self.collection = self.db[MONGO_collection]
        
    def data_insert(self, data):
        self.collection.insert(data)

        
class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v001'
    }
    
    def __init__(self):
        super(Handler,self).__init__()
        self.db = MongoDB()

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://music.douban.com/tag/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        pattern = re.compile(r'https://music.douban.com/tag/\w\s*?')
        for each in response.doc('a[href^="https"]').items():
            if re.match(pattern,each.attr.href):
                self.crawl(each.attr.href,
                     callback=self.list_page)
    
    def list_page(self, response):
        pattern = re.compile(r'https://music.douban.com/subject/\d*?')
        for each in response.doc('a[href^="https"]').items():
            if re.match(pattern,each.attr.href):
                self.crawl(each.attr.href,
                           callback=self.detail_page)
        for each in response.doc('.paginator > a').items():
            self.crawl(each.attr.href,
                       callback=self.list_page)
    


    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('h1 > span').text(),
            "performer" :response.doc('.ckd-collect span > a').text() 
        }
    
    def on_result(self, result):
        if not result:
            return
        self.db.data_insert(result)
