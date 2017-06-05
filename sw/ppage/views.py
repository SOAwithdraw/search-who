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
    return render(request, 'ppage/profile.html', {'p': p, 'news_list': news_list, 'th': search_settings['th']})
