import requests
import json
import time
import math
import hashlib
import random
import string
import pymongo

UA = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
      'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
      'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
      'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
      'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',
      'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TencentTraveler4.0)',
      'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
      'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
      ]

def getASCP():
    t = int(math.floor(time.time()))
    e = hex(t).upper()[2:]
    m = hashlib.md5()
    m.update(str(t).encode(encoding='utf-8'))
    i = m.hexdigest().upper()

    if len(e) != 8:
        AS = '479BB4B7254C150'
        CP = '7E0AC8874BB0985'
        return AS,CP

    n = i[0:5]
    a = i[-5:]
    s = ''
    r = ''
    for o in range(5):
        s += n[o] + e[o]
        r += e[o + 3] + a[o]

    AS = 'A1' + s + e[-3:]
    CP = e[0:3] + r + 'E1'
    return AS,CP


def get_url(max_behot_time,AS,CP):
    url = 'https://www.toutiao.com/api/pc/feed/?' \
          'max_behot_time={0}' \
          '&category=__all__' \
          '&utm_source=toutiao' \
          '&widen=1' \
          '&tadrequire=true' \
          '&as={1}' \
          '&cp={2}' \
          '&_signature=fSx9HAAAJ44hQNL0E6wWF30sfQ'.format(max_behot_time,AS,CP)
    # print(url)
    return url

def get_cookies(headers):
    r = requests.get('https://www.toutiao.com', headers=headers)
    return r.cookies.values()[0]


class MongoDB(object):
    def __init__(self):
        self.client = pymongo.MongoClient('172.17.0.107', 27017)
        self.news = self.client['toutiao']['news']

def get_data(get_time):
    max_behot_time = get_time
    user_agent = random.choice(UA)
    headers = {
        'user-agent': user_agent
    }
    tt_webid = get_cookies(headers)
    cookies = {
        'tt_webid': tt_webid
    }
    db = MongoDB()
    while True:
        AS, CP = getASCP()
        url = get_url(max_behot_time, AS, CP)
        user_agent = random.choice(UA)
        headers = {
            'user-agent': user_agent
        }
        r = requests.session().get(url, headers=headers, cookies=cookies)
        r_record = r.json()
        if r_record and r_record['message']=='success':
            data = r_record['data']
            for i in data:
                find_data = db.news.find_one({'group_id': i['group_id']})
                if find_data:
                    find_data['repeat_count'] = str(int(find_data['repeat_count']) + 1)
                    db.news.update({'group_id': find_data['group_id']}, {'$set': find_data})
                    print('抓取成功:', find_data['title'], '去重次数:', find_data['repeat_count'])
                else:
                    i['repeat_count'] = '0'
                    db.news.insert(i)
                    print('抓取成功：', i['title'], '首次抓取')
            max_behot_time = r_record['next']['max_behot_time']
            time.sleep(1)
        else:
            print(max_behot_time, '抓取失败')
            time.sleep(60)
            get_data(max_behot_time)


if __name__ == '__main__':
    get_data(0)
