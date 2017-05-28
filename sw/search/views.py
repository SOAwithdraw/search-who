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


def restore_person(p):
    return Person_cluster(baike=p.baike, weibo=p.weibo, zhihu=p.zhihu, news=json.loads(p.news), picture=p.picture, keyword=p.keyword, weight=p.weight)


def search_person(request):
    content = request.GET['person']
    print(content.encode('utf-8'))
    contents = content.split()
    name = contents[0]

    data_from_db = Person.objects.filter(name=name)
    if len(data_from_db) == 0:
        if len(contents) > 1:
            result = news_search.search(name, ''.join(contents[1:]))
        else:
            result = news_search.search(name)

        for p in result:
            p_save = Person_model(name=name, baike=p.baike, weibo=p.weibo, zhihu=p.zhihu,
                                  news=json.dumps(p.news), picture=p.picture, keyword=p.keyword,
                                  weight=p.weight)
            p_save.save()
    else:
        result = [restore_person(p) for p in data_from_db]

    return render(request, 'search/result.html', {'name': content, 'pn': len(result), 'result': None})
