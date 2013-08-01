#coding:utf-8
from django.conf.urls import patterns, include, url
from views import cart, cnsgn, buy, delete, checkout, submit

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^consignee\/$', cnsgn),
    (r'^buy\/$', buy),
    (r'^del\/$', delete),
    (r'^checkout\/$', checkout),
    (r'^submit\/$', submit),
)