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

def getpeople(s):

    fr = open('config.yaml', 'r')
    outputfile = codecs.open("baidubaike.html", "w", "utf-8")
    people = []
    
    try:
        p = yaml.load(fr)
        par = p['baidubaike']
        data = urllib.urlencode(par)

        url = p['baidubaikeurl']
        url = url + s + '?' + data
        print url

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'    
        headers = { 'User-Agent' : user_agent }  

        request = urllib2.Request(url)
        request.add_header('User-Agent' , user_agent)
        response = urllib2.urlopen(request)
        html = response.read()
        html = html.decode('utf-8')
        pattern = re.compile(unicode("共[0-9]*个义项", 'utf-8'))
        useful = pattern.findall(html)
        
        uitem = useful[0]
        strcount = ""
        for x in uitem:
            if '0' <= x and x <= '9':
                strcount = strcount + x
        count = int(strcount)
        print count
        if count < 2:
            return people
        for i in range(0, count):
            try:
                person = {}
                k = i+2
                par['force'] = k
                data = urllib.urlencode(par)

                url = p['baidubaikeurl']
                url = url + s + '?' + data
                print url
                time.sleep(1);

                user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'    
                headers = { 'User-Agent' : user_agent }  

                request = urllib2.Request(url)
                request.add_header('User-Agent' , user_agent)
                response = urllib2.urlopen(request)
                html = response.read()
                html = html.decode("utf-8")
                html = html.replace("\n", "")
                html = html.replace("\r", "")
                html = html.replace("&nbsp;", " ")
                html = html.replace("&quot;", "\"")
                html = html.replace("&amp;", "&")
                html = html.replace("&lt;", "<")
                html = html.replace("&gt;", ">")
                pattern = re.compile("<dd class=\"basicInfo-item value\">.*?</dd>")
                messagelist = pattern.findall(html)
                message = []
    
                pattern = re.compile("<div class=\"para\" label-module=\"para\">.*<div class=\"configModuleBanner\">")
                usefullist = pattern.findall(html)
                describe = usefullist[0]
                pattern = re.compile("<.*?>")
                describe = re.sub(pattern, " ", describe)
                for x in messagelist:
                    message.append(re.sub(pattern, "", x))
                person["describe"] = describe
                person["info"] = message
                person["id"] = k
                people.append(person)
                #pattern = re.compile(unicode("<dt class=\"basicInfo-item name\">.*?</dt>","utf-8"))
                outputfile.write(html)
            except:
                pass
            
    except:
        pass
    #html = html.decode("utf-8")
    
    return people

if __name__ == '__main__':
    output = codecs.open("baidubaike.yaml", "w", "utf-8")

    word = unicode('陈驰', 'utf-8')

    #cbegin = datetime.datetime.now()
    searchresult = getpeople(word)
    #cend = datetime.datetime.now()
    #print cend - cbegin

    yaml.dump(searchresult, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)

