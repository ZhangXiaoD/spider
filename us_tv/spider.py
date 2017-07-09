from UrlManager import UrlManager
from HtmlParser import HtmlParser
from DataOutput import DataOutput
import csv


class Spider(object):

    def __init__(self):
        self.manage = UrlManager()

    def spider(self, url, param):
        page_num = HtmlParser.get_page_num(url)
        print('page_num:', page_num)
        with open('./name.csv', 'a') as csvfile:
            fielddnames = ['title', 'url', 'down']
            write = csv.DictWriter(csvfile, fieldnames=fielddnames)
            write.writeheader()
        for i in range(1, page_num+1):
            page_url = url + param + str(i)
            print(page_url)
            new_urls = HtmlParser.get_page_urls(page_url)
            self.manage.add_new_urls(new_urls)
            while self.manage.has_new_url():
                try:
                    new_url = self.manage.get_new_url()
                    data = HtmlParser.get_data(new_url)
                    DataOutput.write_data(data)
                    print(data)
                except Exception as e:
                    print('抓取失败！error:', e)
            print('已经抓取{}条数据'.format(self.manage.old_urls_size()))

if __name__ == '__main__':
    spider = Spider()
    spider.spider('http://cn163.net/ddc1/', 'page/')
