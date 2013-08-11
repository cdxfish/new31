#coding:utf-8
from django.conf.urls import patterns
from views import getItemPin, getSpec, cNum, cLogcs, cOrd, cFnc, cAdv, cDman, cItem, getItemByKeyword, itemLike

urlpatterns = patterns('',
    (r'^itemmore\/$',getItemPin),
    (r'^itemspec\/$',getSpec),  #获取规格
    (r'^cnum\/$', cNum),
    (r'^clogcs\/$', cLogcs),
    (r'^cord\/$', cOrd),
    (r'^cfnc\/$', cFnc),
    (r'^cadv\/$', cAdv),
    (r'^cdman\/$', cDman),
    (r'^citem\/$', cItem),
    (r'^item\/$', getItemByKeyword),
    (r'^like\/$', itemLike),
)