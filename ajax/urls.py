#coding:utf-8
from django.conf.urls import patterns, url
from new31.func import pPatterns

from views import getItemPin, itemLike, getSpec, cNum, cLogcs, cFnc, cItem, cOrd, cAdv, cDman, getItemByKeyword, getUser

urlpatterns = pPatterns(
        (r'^itemmore\/$', getItemPin, 'ajaxGetItemPin', 0),
        (r'^like\/$', itemLike, 'ajaxItemLike', 0),
        (r'^itemspec\/$',getSpec, 'ajaxgetSpec', 0),  #获取规格
        (r'^cnum\/$', cNum, 'ajaxChNum', 0),
        (r'^clogcs\/$', cLogcs, 'ajaxChLogcs', 0),
        (r'^cfnc\/$', cFnc, 'ajaxChFnc', 0),
        (r'^citem\/$', cItem, 'ajaxChItem', 0),     
        (r'^cord\/$', cOrd, 'ajaxChOrd', 1),
        (r'^cadv\/$', cAdv, 'ajaxChAdv', 1),
        (r'^cdman\/$', cDman, 'ajaxDman', 1),
        (r'^item\/$', getItemByKeyword, 'ajaxGetItem', 1),
        (r'^user\/$', getUser, 'ajaxGetUser', 1)
    )