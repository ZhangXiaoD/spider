from UrlManager import UrlManager
from DataOutput import DataOutput
from HtmlParser import HtmlParser
import time


class Spider(object):

    def __init__(self):
        self.manage = UrlManager()
        self.output = DataOutput()
        self.parse = HtmlParser()

    def crawl(self):
        print(self.parse.page_num)
        for i in range(1, self.parse.page_num+1):
            new_urls = self.parse.get_page_urls(i)
            print(new_urls)
            self.manage.add_new_urls(new_urls)
            while self.manage.has_new_url():
                new_url = ''
                try:
                    new_url = self.manage.get_new_url()
                    print(new_url)
                    data = self.parse.get_data(new_url)
                    print(data)
                    self.output.save_mongo(data)
                    time.sleep(1)
                except Exception as e:
                    print('抓取失败：', new_url, e)
        print('已经抓取{}条数据'.format(self.output.data_size()))

if __name__ == '__main__':
    spider = Spider()
    spider.crawl()
