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

def getuser(s):

    fr = open('config.yaml', 'r')
    outputfile = codecs.open("zhihuuser.html", "w", "utf-8")

    p = yaml.load(fr)
    par = p['zhihuuser']
    par['q'] = s;
    data = urllib.urlencode(par)

    url = p['zhihuuserurl']
    url = url + '?' + data
    print url

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'    
    headers = { 'User-Agent' : user_agent }  

    request = urllib2.Request(url)
    request.add_header('User-Agent' , user_agent)
    response = urllib2.urlopen(request)
    html = response.read()
    pattern = re.compile("<li class=\"item.*?</li>")
    alluser = pattern.findall(html)
    
    users = []
    for x in alluser:
        zhihuuser = {}
        pattern = re.compile("<img src=.*?>")
        img = pattern.findall(x)
        pattern = re.compile("\".*?\"")
        imgs = pattern.findall(img[0])
        zhihuuser["img"] = imgs[0][1:-1]
        pattern = re.compile("<.*?>")
        x = re.sub(pattern, "$", x)
        x = x.replace("$$", "$")
        things = x.split('$')
        useful = []
        for y in things:
            if y != "":
                useful.append(y)
                if(len(useful) == 2):
                    if (useful[1][0] >= '0' and useful[1][0] <= '9'):
                        useful[1] = ""
                        useful.append(y)

        zhihuuser['name'] = useful[0].decode('utf-8')
        zhihuuser['info'] = useful[1].decode('utf-8')
        zhihuuser['reply'] = useful[2]
        zhihuuser['pn'] = useful[4]
        zhihuuser['fans'] = useful[6]
        users.append(zhihuuser)
        outputfile.write('\n')
    
    #html = html.decode("utf-8")
    
    return users

if __name__ == '__main__':
    output = codecs.open("zhihuuser.yaml", "w", "utf-8")

    word = unicode('唐杰', 'utf-8')

    #cbegin = datetime.datetime.now()
    searchresult = getuser(word)
    #cend = datetime.datetime.now()
    #print cend - cbegin

    yaml.dump(searchresult, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)

