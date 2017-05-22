# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

import os
import sys
sys.path.append('search/code')
import news_search


def redirect_homepage(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    return render(request, 'search/index.html')


def search_person(request):
    content = request.GET['person']
    print(content.encode('utf-8'))
    contents = content.split()
    name = contents[0]
    '''
    if len(contents) > 1:
        result = news_search.search(name, ''.join(contents[1:]))
    else:
        result = news_search.search(name)
    '''
    for i in range(int(1e7)):
        pass
    result = [['清华大学计算机系', [('url11', 'title11'), ('url12', 'title12')]],
              ['FF14终身优秀玩家', [('url21', 'title21'), ('url22', 'title22')]],
              ['资深睡眠大师', [('url31', 'title31'), ('url32', 'title32')]],
              ['美食及外卖协会现任董事长', [('url41', 'title41'), ('url42', 'title42')]]]
    return render(request, 'search/result.html', {'name': content, 'pn': len(result), 'result': result})
