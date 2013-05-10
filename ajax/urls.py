#coding:utf-8
from django.conf.urls import patterns, include, url
from views import *
from cart.views import *

urlpatterns = patterns('',
    (r'^itemmore\/$',getLineItemMore),
    (r'^itemspec\/(?P<t>\d{1})(?P<i>\d+)\/$',getItemSpec),  #获取规格
    # (r'^buy\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': buyItemToCart}), #购买商品
    # (r'^clear\/(?P<t>\d{1})(?P<i>\d+)\/$', ajaxCartItem,  {'f': clearCartItem}), #删除商品
    (r'^itemnum\/(?P<t>\d+)\/(?P<i>\d+)\/$', ajaxCartItemNum,  {'f': changeCartItem}),
    (r'^ccon\/$', cConsigneeByAjax),
    (r'^item\/$', getItemByKeyword),
)