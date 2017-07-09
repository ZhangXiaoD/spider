class UrlManager(object):

    def __init__(self):
        # 未爬取url集合
        self.new_urls = set()
        # 已爬取url集合
        self.old_urls = set()

    def has_new_url(self):
        '''
        判断是否有未爬取的url
        :return:
        '''
        return self.new_urls_size() != 0

    def new_urls_size(self):
        '''
        判断未爬取url集合的大小
        :return:
        '''
        return len(self.new_urls)

    def old_urls_size(self):
        '''
        判断已爬取url集合的大小
        :return:
        '''
        return len(self.old_urls)

    def get_new_url(self):
        '''
        获取一个未爬取的url
        :return:
        '''
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        '''
        把新的URL添加到未爬取的url集合中
        :param url: 单个url
        :return:
        '''
        if url is None:
            return
        if url not in self.old_urls and url not in self.new_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        '''
        把新的url添加到未爬取的url集合中
        :param urls: url集合
        :return:
        '''
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)
