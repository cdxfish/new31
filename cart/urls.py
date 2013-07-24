#coding:utf-8
from django.conf.urls import patterns, include, url
from views import cart, cnsgn, buy, clear, checkout, submit

urlpatterns = patterns('',
    (r'^$', cart),
    (r'^consignee\/$', cnsgn),
    (r'^buy\/(?P<specID>\d+)\/$', buy),
    (r'^clear\/(?P<mark>\d+)\/$', clear),
    (r'^checkout\/$', checkout),
    (r'^submit\/$', submit),
)