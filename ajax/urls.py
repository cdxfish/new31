#coding:utf-8
from django.conf.urls import patterns, url
from new31.func import pPatterns

from views import reToURL

urlpatterns = pPatterns(
        (r'^reverse\/$', reToURL, 1)
    )