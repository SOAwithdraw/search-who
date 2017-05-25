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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.action_chains import ActionChains

# 先调用无界面浏览器PhantomJS或Firefox
#driver = webdriver.PhantomJS(executable_path="G:\phantomjs-1.9.1-windows\phantomjs.exe")

# 全局变量 文件操作读写信息
#****************************************************************


def VisitPersonPage(s, t = 20):
    try:
        print u'准备访问个人网站.....'

        driver = webdriver.Firefox()
        wait = ui.WebDriverWait(driver, 10)

        driver.get(u"https://m.weibo.cn/p/100103type=3&q="+s+"?type=user")
        time.sleep(5)
        
        for times in range(0, t/10):
            js="var q=document.documentElement.scrollTop=10000"  
            driver.execute_script(js) 
            time.sleep(1)
        
        str_name = driver.find_element_by_id("app")
        messages = str_name.text.split('\n')
        html = driver.page_source
        pattern = re.compile("<img src=.*?>")
        imgs = pattern.findall(html)
        weibolist = []
        for x in range(1, len(imgs)):
            ix = x * 4 - 2
            weibo = {}
            weibo['name'] = messages[ix]
            weibo['info'] = messages[ix+1]
            
            weibo['img'] = imgs[x][10:-2].encode('utf-8')
            weibo['id'] = x
            weibolist.append(weibo)

        output = codecs.open("weibo.yaml", "w", "utf-8")
        yaml.dump(weibolist, default_flow_style=False,stream=output,indent=4,encoding='utf-8',allow_unicode=True, width=1000)
        
    except Exception, e:
        print "Error: ", e
    finally:
        driver.close()
        
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
    
    VisitPersonPage(u'郭文景', 30)
