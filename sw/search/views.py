# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

import sys
sys.path.append('search/code')
import news_search


def redirect_homepage(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    return render(request, 'search/index.html')


def search_person(request):
    content = request.GET['person']

    return HttpResponse(content)
