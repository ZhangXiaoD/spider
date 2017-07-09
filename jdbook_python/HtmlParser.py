import re
from HtmlDownloader import HtmlDownloader
from bs4 import BeautifulSoup


class HtmlParser(object):

    def __init__(self):
        self.downloader = HtmlDownloader()
        self.page_num = self._get_page_num()

    def _get_page_num(self):
        data = self.downloader.get_page(1)
        if data and 'value' in data.keys():
            count = re.search(r',"wareCount":(\d*?),"', data['value']).groups()[0]
            if count:
                count = int(count)
                num = count % 10
                if num == 0:
                    return num
                else:
                    return count//10+1

    def get_page_urls(self, page):
        urls = []
        url = ''
        data = self.downloader.get_page(page)
        pattern = re.compile(r',\"eBookFlag\":(.*?),\".*?,"wareId":"(\d*?)"')
        result = re.findall(pattern, data['value'])
        if result:
            for item in result:
                if item[0] == 'true':
                    url = 'https://e.m.jd.com/ebook/' + item[1] + '.html'
                if item[0] == 'false':
                    url = 'https://item.m.jd.com/product/' + item[1] + '.html'
                urls.append(url)
        return urls

    def get_data(self, url):
        html = self.downloader.get_page_data(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = ''
        price = '0'
        if url[0:12] == 'https://e.m.':
            title = soup.find('p', class_='db-title').text
            price = soup.find('span', class_='db-price-num').text
        if url[0:12] == 'https://item':
            title = soup.find('span', class_='title-text').text
            price = float(soup.find('span', class_='big-price').text)+float(soup.find('span', class_='small-price').text)
        if price == None:
            price = '0'
        data = {
            'title': title,
            'price': price,
            'url': url
        }
        return data
