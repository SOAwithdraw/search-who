# coding=utf-8

"""   
Created on 2016-02-22 @author: Eastmount 
 
功能: 爬取新浪微博用户的信息 
信息：用户ID 用户名 粉丝数 关注数 微博数 微博内容 
网址：http://weibo.cn/ 数据量更小 相对http://weibo.com/ 
 
"""

import time
import re
import os
import sys
import codecs
import shutil
import urllib
import yaml
import urllib2
from chardet import detect

# 先调用无界面浏览器PhantomJS或Firefox
#driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")

# 全局变量 文件操作读写信息
#****************************************************************

reload(sys)
sys.setdefaultencoding("utf-8")


def VisitPersonPage(s):
    try:

        if not os.path.exists("newweiboresult/"):
            os.mkdir("newweiboresult")

        fr = open('config.yaml', 'r')
        ya = yaml.load(fr)
        data = ya['newweibo']
        data['nickname'] = s

        urldata = urllib.urlencode(data)
        url = ya['newweibourl'] + urldata

        print url

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
        headers = {'User-Agent': user_agent}

        request = urllib2.Request(url)
        request.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(request)
        html = response.read()

        #html = html.replace("\n", "")
        #html = html.replace("\r", "")
        html = html.replace("&nbsp;", " ")
        html = html.replace("&quot;", "\"")
        html = html.replace("&amp;", "&")
        html = html.replace("&lt;", "<")
        html = html.replace("&gt;", ">")
        weibolist = []
        outhtml = codecs.open("weibo.html", "w", "utf-8")
        sp = "<div class=\\\"list_person"
        listhtml = html.split(sp)
        outhtml.write(html)
        for listcnt in range(1, len(listhtml)):
            html = listhtml[listcnt]
            pattern = re.compile(">[0-9]+?\\\\?u?[a-f0-9]*?<\\\\/a>")
            messages = pattern.findall(html)
            me = []
            for x in messages:
                x = x.encode('utf8')
                me.append(x[1:-5].encode('utf-8'))
            pattern = re.compile("src=\\\\\"(http:\\\\/\\\\/tva.*?)\"")
            imgs = pattern.findall(html)
            img = []
            for x in imgs:
                img.append(x.replace("\\", ""))
            pattern = re.compile("href=[^\"]*?\"[^\"]*?\" title=[^\"]*?\"[^\"]*?\"")
            users = pattern.findall(html)

            user = {}
            cnt = 0
            info = ""
            pattern = re.compile("<p class=\\\\\"person_card\\\\\">(.*?)<\\\\/p>")
            infos = pattern.findall(html)
            try:
                info = info + infos[0].decode('unicode_escape') + " "
            except:
                pass

            pattern = re.compile("<div class=\\\\\"person_info\\\\\">(.*?)<\\\\/p>")
            infos = pattern.findall(html)
            try:
                info = info + infos[0].decode('unicode_escape')
            except:
                pass
            info = info.replace("\n", "")
            info = info.replace("\t", "")
            user['info'] = info
            for x in users:
                x = x.replace("\\u", "$")
                x = x.replace("\\", "")
                x = x.replace("$", "\\u")

                al = x.split('\"')
                url = al[1]
                name = al[3]
                if 'refer_flag' in url:
                    cnt = cnt + 1
                    if(cnt % 2 == 0):
                        user['name'] = name.decode('unicode_escape')
                        user['img'] = img[((cnt / 2) - 1)]
                        user['url'] = url
                        user['guanzhu'] = me[((cnt / 2) - 1) * 3]
                        user['fans'] = me[((cnt / 2) - 1) * 3 + 1].decode('unicode_escape')
                        user['weibo'] = me[((cnt / 2) - 1) * 3 + 2]
            weibolist.append(user)

        output = codecs.open("weibo.yaml", "w", "utf-8")
        yaml.dump(weibolist, default_flow_style=False, stream=output, indent=4, encoding='utf-8', allow_unicode=True, width=1000)

        savefile = codecs.open("newweiboresult/%s.yaml" % (s), "w", "utf-8")
        yaml.dump(weibolist, default_flow_style=False, stream=savefile, indent=4, encoding='utf-8', allow_unicode=True, width=1000)
        return weibolist
    except Exception, e:
        print "Error: ", e
    finally:
        print u'End\n\n'
        print '**********************************************\n'

#*************************************************************************
#                                程序入口 预先调用
#*************************************************************************


if __name__ == '__main__':

    # 定义变量
    username = '18611607626'  # 输入你的用户名
    password = 'soawithdraw'  # 输入你的密码
    user_id = 'soawithdraw'  # 用户id url+id访问个人

    # 在if __name__ == '__main__':引用全局变量不需要定义 global inforead 省略即可

    VisitPersonPage(u'陈驰')
