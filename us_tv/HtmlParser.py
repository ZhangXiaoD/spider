import re
from HtmlDownloader import HtmlDownloader
from bs4 import BeautifulSoup


class HtmlParser(object):

    @staticmethod
    def get_page_num(url):
        '''
        获取page总数
        :param url: base url
        :return:
        '''
        html = HtmlDownloader.download(url)
        soup = BeautifulSoup(html, 'html.parser')
        num = int(soup.find(title='最后一页').text)
        return num

    @staticmethod
    def get_page_urls(url):
        '''
        获取网页内的目标urls
        :param url: 目标网页的url
        :return:
        '''
        tv_urls = set()
        html = HtmlDownloader.download(url)
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.find_all('div', class_='archive_title')
        for link in links:
            tv_urls.add(link.h2.a['href'])
        return tv_urls

    @staticmethod
    def get_data(url):
        '''
        获取目标网页的信息
        :param url: 目标网页的url
        :return:
        '''
        data = {}
        html = HtmlDownloader.download(url)
        soup = BeautifulSoup(html, 'html.parser')
        data['title'] = soup.title.text
        data['url'] = url
        tv_data = soup.find_all(href=re.compile(r'S\d\dE\d\d'))
        if tv_data:
            down_datas = {}
            for tv in tv_data:
                down_datas[tv.text] = tv['href']
            data['down'] = down_datas
        return data
