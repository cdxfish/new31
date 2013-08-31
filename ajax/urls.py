#coding:utf-8
from django.conf.urls import patterns, url
from new31.func import pPatterns

from views import getItemPin, itemLike, getSpec, cNum, cLogcs, cFnc, cItem, cOrd, cAdv, cDman, getItemByKeyword, getUser

urlpatterns = pPatterns(
        (r'^itemmore\/$', getItemPin, 0),
        (r'^like\/(?P<id>\d+)\/$', itemLike, 0),
        (r'^itemspec\/(?P<id>\d+)\/$',getSpec, 0),  #获取规格
        (r'^cnum\/$', cNum, 0),
        (r'^clogcs\/$', cLogcs, 0),
        (r'^cfnc\/$', cFnc, 0),
        (r'^citem\/$', cItem, 0),     
        (r'^cord\/$', cOrd, 1),
        (r'^cadv\/$', cAdv, 1),
        (r'^cdman\/$', cDman, 1),
        (r'^item\/$', getItemByKeyword, 1),
        (r'^user\/$', getUser, 1)
    )