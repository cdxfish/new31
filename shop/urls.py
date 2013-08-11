#coding:utf-8
from django.conf.urls import patterns
from views import shop

urlpatterns = patterns('',
    (r'^$', shop),
)