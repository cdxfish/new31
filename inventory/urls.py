#coding:utf-8
from django.conf.urls import patterns
from views import iUI, iList, cOnl, default, minus, plus

urlpatterns = patterns('',
    (r'^$', iUI),
    (r'^list\/$', iList),
    (r'^conl\/$', cOnl),
    (r'^default\/$', default),
    (r'^minus\/$', minus),
    (r'^plus\/$', plus),
)