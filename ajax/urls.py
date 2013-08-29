#coding:utf-8
from django.conf.urls import patterns, url
from new31.func import pPatterns

from views import getItemPin, itemLike, getSpec, cNum, cLogcs, cFnc, cItem, cOrd, cAdv, cDman, getItemByKeyword, getUser

urlpatterns = pPatterns(
        (r'^itemmore\/$', getItemPin, 'getItemPin', 0),
        (r'^like\/$', itemLike, 'itemLike', 0),
        (r'^itemspec\/$',getSpec, 'getSpec', 0),  #获取规格
        (r'^cnum\/$', cNum, 'cNum', 0),
        (r'^clogcs\/$', cLogcs, 'cLogcs', 0),
        (r'^cfnc\/$', cFnc, 'cFnc', 0),
        (r'^citem\/$', cItem, 'cItem', 0),     
        (r'^cord\/$', cOrd, 'cOrd', 0),
        (r'^cadv\/$', cAdv, 'cAdv', 0),
        (r'^cdman\/$', cDman, 'cDman', 0),
        (r'^user\/$', getUser, 'getUser', 0),
        (r'^item\/$', getItemByKeyword, 'getItemByKeyword', 0),
    )