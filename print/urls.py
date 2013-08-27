#coding:utf-8
from django.conf.urls import patterns
from views import prntOrd

urlpatterns = patterns('',
    (r'^$', prntOrd),
)