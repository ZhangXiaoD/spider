import requests
from config import KEYWORD
import time

class HtmlDownloader(object):

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'}

    def get_page(self, page):
        """
        获取网页内容
        :param page:搜索页数
        :return:
        """
        data = {
            '_format_': 'json',
            'configuredFilters': '[{"bodyValues":"1","bodyKey":"self"}]',
            'keyword': KEYWORD,
            'page': page
        }
        url = 'https://so.m.jd.com/ware/searchList.action'
        while True:
            r = requests.post(url, headers=self.headers, data=data)
            if r.status_code == 200 and r.history == []:
                r.encoding = 'utf-8'
                return r.json()
            time.sleep(5)

    def get_page_data(self, url):
        while True:
            r = requests.get(url, headers=self.headers)
            if r.status_code == 200 and r.history == []:
                r.encoding = 'utf-8'
                return r.text
            time.sleep(5)