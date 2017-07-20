#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-12 15:19:17
# Project: 163_music

from pyspider.libs.base_handler import *
import pymongo


MONGO_host = '127.0.0.1'
MONGO_port = 27017
MONGO_db = '163_music'


class MongoDB(object):
    
    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_host,MONGO_port)
        self.db = self.client[MONGO_db]
        
    def data_insert(self, type, name, data):
        self.db[type].update({name:data.get(name)},{'$set':data},upsert=True)
    

class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v001',
        'headers': {
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:51.0) Gecko/20100101 Firefox/51.0'
        }
    }
    
    def __init__(self):
        super(Handler, self).__init__()
        self.db = MongoDB()


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://music.163.com/discover/playlist', callback=self.index_page)

    @config(age=24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.msk').items():
            self.crawl(each.attr.href, callback=self.playlist_page)
        for each in response.doc('.u-page > a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.index_page)
    
    @config(age=5 * 24 * 60 * 60)
    def playlist_page(self, response):
        music_list = []
        for each in response.doc('.f-hide > li > a').items():
            music_list.append([each.text(),each.attr.href])
            self.crawl(each.attr.href, callback=self.detail_page)
        for each in response.doc('ul.m-rctlist.f-cb > li > .info > .f-thide > a').items():
            self.crawl(each.attr.href, callback=self.playlist_page)
        return {
            'url': response.url,
            'type': 'playlist',
            'title': response.doc('title').text(),
            'playlist_name': response.doc('h2.f-ff2.f-brk').text(),
            'tags': [x.text() for x in response.doc('.tags.f-cb > a').items()],
            'present': response.doc('#album-desc-more').text()[4:],
            'music_list': music_list,
            'music_count': len(music_list),
            'collect': response.doc('#content-operation > a:eq(2) > i').text().strip('()'),
            'share': response.doc('#content-operation > a:eq(3) > i').text().strip('()'),
            'comment_count': response.doc('#cnt_comment_count').text(),
            'play_count': response.doc('#play-count').text()
            
        }
    
    @config(age=5 * 24 * 60 * 60)
    def album_page(self, response):
        music_list = []
        for each in response.doc('.f-hide > li > a').items():
            music_list.append([each.text(),each.attr.href])
            self.crawl(each.attr.href, callback=self.detail_page)
        self.crawl(response.doc('.intr > span > .s-fc7').attr.href, callback=self.artist_page)
        return {
            'url': response.url,
            'type': 'album',
            'title': response.doc('title').text(),
            'album_name': response.doc('h2.f-ff2').text(),
            'singer': response.doc('.intr > span > .s-fc7').text(),
            'publish_time': response.doc('.topblk > p:eq(1)').text().split(' ')[1],
            'publish_company': response.doc('.topblk > p:eq(2)').text().split(' ',1)[1] if response.doc('.topblk > p:eq(2)') else '',
            'present': response.doc('.n-albdesc > p.f-brk').text(),
            'music_list': music_list,
            'music_count': len(music_list),
            'comment_count': response.doc('#cnt_comment_count').text()
        }
    
    @config(age=10 * 24 * 60 * 60)
    def artist_page(self, response):
        for each in response.doc('.f-hide > li > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        self.crawl(response.doc('ul#m_tabs > li:eq(1) > a').attr.href, callback=self.artist_album_page)
    
    @config(age=10 * 24 * 60 * 60)
    def artist_album_page(self, response):
        for each in response.doc('.msk').items():
            self.crawl(each.attr.href, callback=self.album_page)
        for each in response.doc('.u-page > a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.artist_album_page)

    def detail_page(self, response):
        self.crawl(response.doc('.m-lycifo > .f-cb > .cnt > p:eq(1) > a').attr.href, callback=self.album_page)
        return {
            "url": response.url,
            'type': 'song',
            "title": response.doc('title').text(),
            'song_name': response.doc('em.f-ff2').text(),
            'singer': response.doc('.m-lycifo > .f-cb > .cnt > p:eq(0) > span > a').text(),
            'album': response.doc('.m-lycifo > .f-cb > .cnt > p:eq(1) > a').text()
        }
    
    def on_result(self, result):
        if not result:
            return
        type = result['type']
        name = type + '_name'
        self.db.data_insert(type, name, result)

