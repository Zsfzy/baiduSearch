# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

def debugDump(text):
    f = open('dump.htm', 'w+', encoding='utf-8')
    f.write(text)
    f.close()

class baiduSearch(object):
    def __init__(self, pn=0, rn=50):
        self.pn = pn
        self.rn = rn

    def search(self, key):
        # 搜索关键字
        text = self.getData(key, self.pn, self.rn)

        # 检查数据是否正常接收
        if text == False:
            return False

        # 过滤数据
        data = self.filterData(text)
        # 返回数据
        return data

    def getData(self, key, pn=0, rn=50):
        agent = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
        headers = {'User-Agent': agent}
        timeout = 10

        url = "https://www.baidu.com/s?ie=utf-8&rn=%d&wd=%s" %(rn, key)
        if pn != 0:
            url += '&pn=%d' %(pn)

        r = requests.get(url, headers = headers, timeout=timeout)
        if r.status_code != 200:
            print("抓取错误，网络状态码:%d。" % (r.status_code))
            return False
        self.pn += rn
        return r.text

    def filterData(self, text):
        text = BeautifulSoup(text, 'lxml')
        arr = text.find_all(class_ = 'result c-container ')
        regexes = re.compile(r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}')
        arrDomain = []
        for i in arr:
            t = i.find(class_ = 't')
            title = t.text
            url = t.a['href']
            domain = i.find(class_ = 'c-showurl').text
            m = regexes.search(domain)
            
            if m:
                domain = m.group(0)
            else:
                print('域名正则规则无法适配！')
                debugDump(domain)
                continue
            arrDomain.append({'title': title, 'domain': domain, 'url': url})
            
        if arrDomain == []:
            return False
        return arrDomain


if __name__ == "__main__":
    print(baiduSearch().search('Python'))
    
