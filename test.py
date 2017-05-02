#coding: utf-8
import sys
import urllib
import urllib2
from bs4 import BeautifulSoup

question_word = "cc"
url = "http://www.baidu.com/s?wd=" + urllib.quote(unicode(question_word, 'utf-8'))
htmlpage = urllib2.urlopen(url).read()
print htmlpage