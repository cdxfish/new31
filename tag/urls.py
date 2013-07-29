#coding:utf-8
from django.conf.urls import patterns
from views import randomShow, tagShow

urlpatterns = patterns('',
    (r'^$', randomShow),
    (r'^(?P<tag>.*)\/$',tagShow),
)