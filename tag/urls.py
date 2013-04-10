#coding:utf-8
from django.conf.urls import patterns
from views import *

urlpatterns = patterns('',
    (r'^tag\/$', tagAdmin),
    (r'^$',tag),
    (r'^(?P<tagTitle>.*)\/$',tag),
)