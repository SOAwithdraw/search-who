"""sw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from search import views as search_view
from ppage import views as page_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', search_view.redirect_homepage),
    url(r'^index/$', search_view.index, name='index'),
    url(r'^search/$', search_view.search_person, name='search_person'),
    url(r'^profile/(\d+)$', page_view.profile, name='profile'),
    url(r'^resetting/$', search_view.resetting, name='resetting')
]
