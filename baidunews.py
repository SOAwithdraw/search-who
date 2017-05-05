# -*- coding: utf-8 -*-

import urllib
import urllib2
import yaml
import codecs
import re
import sys
import time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


def get(s):
    fr = open('config.yaml', 'r')
    p = yaml.load(fr)
    par = p['baidunews']
    par['word'] = s

    data = urllib.urlencode(par)

    url = p['baidunewsurl']
    url = url + '?' + data
    # print url

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
    headers = {'User-Agent': user_agent}

    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    response = urllib2.urlopen(request)
    html = response.read()
    #html = html.decode("utf-8")

    soup = BeautifulSoup(html)

    newsurl = []
    text = ""
    for u in soup.find_all('a'):
        if "http://cache.baidu.com/" in u['href']:
            text += u['href'] + '\n'
            newsurl.append(u['href'])
    text += '********************\n'

    result = []
    for newsurlitem in newsurl:
        request = urllib2.Request(newsurlitem)
        request.add_header('User-Agent', user_agent)
        print newsurlitem
        time.sleep(1)
        response = urllib2.urlopen(request)
        html = response.read()
        # print html
        html = html.replace("\n", "")
        html = html.replace("\r", "")

        pattern = re.compile("<p.*?</p>")
        gp = re.findall(pattern, html)

        text = []
        img = []
        for u in gp:
            u = u.decode('gbk', 'ignore')
            soup0 = BeautifulSoup(u)
            ut = soup0.get_text().strip()
            if s in ut:
                text.append(ut)
            if 'img' in u:
                try:
                    img.append(soup0.img['src'])
                except:
                    print newsurlitem
                    pass
        eachnews = {}
        eachnews['text'] = text
        eachnews['img'] = img
        result.append(eachnews)
    return result

output = codecs.open("search.yaml", "w", "utf-8")

word = unicode('陈驰', 'utf-8')

searchresult = get(word)

yaml.dump(searchresult, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)
