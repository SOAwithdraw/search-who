# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Person(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=30)
    baike = models.TextField(verbose_name="百度百科")
    weibo = models.TextField(verbose_name="新浪微博")
    zhihu = models.TextField(verbose_name="知乎")
    news = models.TextField(verbose_name="新闻")
    picture = models.TextField(verbose_name="图片")
    keyword = models.TextField(verbose_name="关键字")
    weight = models.FloatField()

    def __unicode__(self):
        return self.name + ' ' + self.keyword
