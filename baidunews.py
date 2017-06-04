# -*- coding: utf-8 -*-

import urllib
import urllib2
import yaml
import codecs
import re
import sys
import datetime
import time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding( "utf-8" )

def getnews(s, s0, newscnt = 10):
    fr = open('config.yaml', 'r')
    p = yaml.load(fr)
    par = p['baidunews']
    par['word'] = s0
    par['rn'] = newscnt
    data = urllib.urlencode(par)

    url = p['baidunewsurl']
    url = url + '?' + data
    #print url

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'    
    headers = { 'User-Agent' : user_agent }  

    request = urllib2.Request(url)
    request.add_header('User-Agent' , user_agent)
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
    print text
    result = []
    for newsurlitem in newsurl:
        try:
            request = urllib2.Request(newsurlitem)
            request.add_header('User-Agent' , user_agent)
            #print newsurlitem
            time.sleep(1);
            response = urllib2.urlopen(request)
            html = response.read()
            #print html
            html = html.replace("\n", "")
            html = html.replace("\r", "")
            html = html.replace("&nbsp;", " ")
            html = html.replace("&quot;", "\"")
            html = html.replace("&amp;", "&")
            html = html.replace("&lt;", "<")
            html = html.replace("&gt;", ">")
            #html.encode("utf-8")
            pattern = re.compile("<p.*?</p>")
            gp = re.findall(pattern, html)

            text = []
            img = []
            for u in gp:
                u = u.decode('gbk', 'ignore')
                soup0 = BeautifulSoup(u)
                ut = soup0.get_text()
                if s in ut:
                    text.append(ut)
                if 'img' in u:
                    try:
                        imgurl = soup0.img['src']
                        if (imgurl[0] == '/' and imgurl[1] == '/'):
                            imgurl = 'http:' + imgurl
                        img.append(imgurl)
                    except:
                        print newsurlitem
                        pass
            eachnews = {}
            eachnews['text'] = text
            eachnews['img'] = img
            pattern = re.compile("<title.*?</title>")
            newstitle = re.search(pattern, html)
            newstitle = newstitle.group(0)
            pattern = re.compile("<.*?>", re.M)
            ntitle = re.sub(pattern, "", newstitle)
            eachnews['title'] = ntitle.decode('gbk', 'ignore')
            eachnews['url'] = newsurlitem
            print ntitle
            result.append(eachnews)
        except Exception, e:
            print e
    return result

def get(word, cnt):
    x = cnt/5
    word163 = word + " site:163.com"
    wordsina = word + " site:sina.com"
    wordqq = word + " site:qq.com"
    wordfh = word + " site:ifeng.com"
    wordsh = word + " site:sohu.com"
    result = []
    result = result + getnews(word, word163,x)
    result = result + getnews(word, wordsina,x)
    result = result + getnews(word, wordqq,x)
    result = result + getnews(word, wordfh,x)
    result = result + getnews(word, wordsh,x)
    return result


if __name__ == '__main__':
    output = codecs.open("search.yaml", "w", "utf-8")

    word = unicode('唐杰', 'utf-8')

    #cbegin = datetime.datetime.now()
    searchresult = get(word, 50)
    #cend = datetime.datetime.now()
    #print cend - cbegin

    yaml.dump(searchresult, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)

