# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from search.models import Person as Person_model

import os
import sys
import json
sys.path.append('search/code')
import news_search
from cluster import Person as Person_cluster


def redirect_homepage(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    return render(request, 'search/index.html')


def fake_data():
    tj1 = Person_cluster(baike='http://baike.baidu.com/item/%E5%94%90%E6%9D%B0/12019960',
                         weibo='http://weibo.com/jietangthu', zhihu='',
                         news=[['清华大学—中国工程院“知识智能联合研究中心”成立仪式成功举行', 'http://news.sciencenet.cn/htmlnews/2017/5/377417.shtm']],
                         picture='http://imgsrc.baidu.com/baike/pic/item/1b4c510fd9f9d72a6bbe6730d62a2834359bbbc0.jpg',
                         keyword='清华大学 计算机系',
                         weight=1.0)
    tj2 = Person_cluster(baike='http://baike.baidu.com/item/%E5%94%90%E6%9D%B0/1848946',
                         weibo='', zhihu='',
                         news=[['唐杰谈历史与经济:创新增长的制度与理念', 'http://finance.ifeng.com/a/20170421/15313457_0.shtml'],
                               ['专访深圳前副市长唐杰: 深圳经验:市场化、法治化为核心 开放的...', 'http://finance.sina.com.cn/roll/2016-12-26/doc-ifxyxvcr7554355.shtml']],
                         picture='https://imgsa.baidu.com/baike/w%3D268/sign=2018b6261d950a7b753549c232d1625c/d6ca7bcb0a46f21fd219b343f6246b600c33aef5.jpg',
                         keyword='深圳市副市长',
                         weight=0.9)
    tj3 = Person_cluster(baike='http://baike.baidu.com/item/%E5%94%90%E6%9D%B0/1849008',
                         weibo='', zhihu='',
                         news=[['叙永县县长唐杰率队督查安全生产工作', 'http://lz.newssc.org/system/20170426/002166556.html']],
                         picture='https://imgsa.baidu.com/baike/c0%3Dbaike72%2C5%2C5%2C72%2C24/sign=c02973cf4f540923be646b2cf331ba6c/3812b31bb051f819cb808ea6dcb44aed2f73e7b1.jpg',
                         keyword='叙永县县长',
                         weight=0.7)

    return [tj1, tj2, tj3]


def search_person(request):
    content = request.GET['person']
    print(content.encode('utf-8'))
    contents = content.split()
    name = contents[0]

    data_from_db = Person_model.objects.filter(name=name)
    if len(data_from_db) == 0:
        if len(contents) > 1:
            result = news_search.search(name, ''.join(contents[1:]))
        else:
            result = news_search.search(name)
        # result = fake_data()
        for p in result:
            p_save = Person_model(name=name, baike=p.baike, weibo=p.weibo, zhihu=p.zhihu,
                                  news=json.dumps(p.news), picture=p.picture, keyword=p.keyword,
                                  weight=p.weight)
            p_save.save()
    else:
        result = data_from_db

    for p in result:
        print(p)

    print(result)
    return render(request, 'search/result.html', {'title': content, 'name': name, 'pn': len(result), 'result': result})
