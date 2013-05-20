#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from cart.views import *

urlpatterns = patterns('',
    (r'^itemmore\/$',getLineItemMore),
    (r'^itemspec\/(?P<specID>\d+)\/$',getItemSpec),  #获取规格
    (r'^itemnum\/(?P<mark>\d+)\/(?P<num>\d+)\/$', ajaxChangNum),
    (r'^ccon\/$', cConsigneeByAjax),
    (r'^item\/$', getItemByKeyword),
)