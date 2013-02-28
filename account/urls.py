#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^login\/$', login,{'template_name': 'login.htm'}),
    (r'^logout\/$', logout),
    # (r'^login$', login),
    (r'^settings\/$', settings),
    (r'^changepwd\/$', changepwd),
    (r'^order\/$', orderList),
    (r'^order\/(\d+)$', orderDetail),
)
