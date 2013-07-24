#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from cart.views import *

urlpatterns = patterns('',
    (r'^itemmore\/$',getItemPin),
    (r'^itemspec\/(?P<specID>\d+)\/$',getItemSpec),  #获取规格
    (r'^itemnum\/(?P<mark>\d+)\/(?P<num>\d+)\/$', ajaxChangNum),
    (r'^ccon\/$', cCnsgnByAjax),
    (r'^cotype\/$', coTypeByAjax),
    (r'^cadvance\/$', cAdv),
    (r'^cdman\/$', cDman),
    (r'^citem\/$', cItemByAjax),
    (r'^item\/$', getItemByKeyword),
)