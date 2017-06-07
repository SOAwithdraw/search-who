# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from search.models import Person as Person_model
import json
from sw.settings import search_settings


def profile(request, idx):
    p = Person_model.objects.get(id=idx)
    news_list = json.loads(p.news)
    keywords = p.keyword.split(';')
    for keyword in keywords:
        if len(keyword) < 2:
            keywords.remove(keyword)
    if len(keywords) > 10:
        keywords = keywords[:5]
    zhihu_info = json.loads(p.zhihu_info)
    if 'img' in zhihu_info and '_m.' in zhihu_info['img']:
        zhihu_info['img'] = zhihu_info['img'].replace('_m.', '.')
    return render(request, 'ppage/profile.html', {'p': p, 'news_list': news_list, 'th': search_settings['th'], 'keywords': keywords, 'zhihu_info': zhihu_info})
