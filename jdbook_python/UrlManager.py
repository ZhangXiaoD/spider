import redis
from config import REDIS_Host, REDIS_Port


class UrlManager(object):

    def __init__(self):
        # 建立redis连接
        self.pool = redis.ConnectionPool(host=REDIS_Host, port=REDIS_Port)
        self.r = redis.Redis(connection_pool=self.pool)

    def has_new_url(self):
        """
        判断是否有未爬取的url
        :return:
        """
        return self.r.scard('new_url') != 0

    def old_urls_size(self):
        """
        判断已爬取url集合的大小
        :return:
        """
        return self.r.scard('old_url')

    def get_new_url(self):
        """
        获取一个未爬取的url
        :return:
        """
        new_url = self.r.spop('new_url')
        self.r.sadd('old_url', new_url)
        return str(new_url, encoding='utf-8')

    def add_new_url(self, url):
        """
        把新的url添加到未爬取的url集合中
        :param url:
        :return:
        """
        if url is None:
            return
        if not self.r.sismember('old_url', url):
            self.r.sadd('new_url', url)
        else:
            print('该url已经被抓取:', url)

    def add_new_urls(self, urls):
        """
        把新的url添加到未爬取的url集合中
        :param urls:
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def del_old_url(self, url):
        self.r.srem('old_url', url)
