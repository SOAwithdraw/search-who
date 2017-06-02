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
        pattern = re.compile("<a target=_blank .*?>")
        useful = pattern.findall(html)
        urllist = []
        if len(useful) < 2:
            return people
        pattern = re.compile("\".*?\"")

        for x in useful:
            he = pattern.findall(x)
            urllist.append(he[0][7:-1])
        count = len(urllist)
        
        pattern = re.compile("<a target=_blank .*?</a>")
        allmessage = pattern.findall(html)

        introduct = []
        for x in allmessage:
            pattern = re.compile("<.*?>")
            th = re.sub(pattern, "", x)
            introduct.append(th.split(u"：")[1])
        for i in range(0, count):
            try:
                person = {}
                url = p['baidubaikeurl']
                url = url + urllist[i]
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
                try:
                    describe = usefullist[0]
                except:
                    describe = ""
                pattern = re.compile("<.*?>")
                describe = re.sub(pattern, " ", describe)
       
                for x in messagelist:
                    message.append(re.sub(pattern, "", x))
                    
                person["describe"] = describe
                person["info"] = message
                person["id"] = i+1
                person["url"] = url
                person["introdution"] = introduct[i]
                people.append(person)
                #pattern = re.compile(unicode("<dt class=\"basicInfo-item name\">.*?</dt>","utf-8"))
                outputfile.write(html)
            except Exception,e:
                print e
            
    except:
        pass
    #html = html.decode("utf-8")
    
    return people

if __name__ == '__main__':
    output = codecs.open("baidubaike.yaml", "w", "utf-8")

    word = unicode('唐杰', 'utf-8')

    #cbegin = datetime.datetime.now()
    searchresult = getpeople(word)
    #cend = datetime.datetime.now()
    #print cend - cbegin

    yaml.dump(searchresult, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)

