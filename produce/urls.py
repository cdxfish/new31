#coding:utf-8
from django.conf.urls import patterns
from views import produceUI, pCons

urlpatterns = patterns('',
    (r'^$', produceUI),
    (r'^(?P<s>\d+)/$', pCons),
)