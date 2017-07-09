import requests


class HtmlDownloader(object):

    @staticmethod
    def download(url):
        '''
        获取网页内容
        :param url: 目标网页的url
        :return:
        '''
        if url is None:
            return None
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/' \
                     '49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            r.encoding = 'utf-8'
            return r.text
        return None
