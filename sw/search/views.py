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
    if len(contents) > 1:
        news_search.search(name, ''.join(contents[1:]))
    else:
        news_search.search(name)
    return HttpResponse(content)
