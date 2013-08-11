#coding:utf-8
from django.conf.urls import patterns
from views import produceUI

urlpatterns = patterns('',
    (r'^$', produceUI),
)