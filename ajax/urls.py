#coding:utf-8
from django.conf.urls import patterns
from views import getItemPin, itemLike, getSpec, cNum, cLogcs, cFnc, cItem, cOrd, cAdv, cDman, getItemByKeyword, getUser

urlpatterns = patterns('',
    (r'^itemmore\/$',getItemPin),
    (r'^like\/$', itemLike),
    (r'^itemspec\/$',getSpec),  #获取规格
    (r'^cnum\/$', cNum),
    (r'^clogcs\/$', cLogcs),
    (r'^cfnc\/$', cFnc),
    (r'^citem\/$', cItem),
    
    (r'^cord\/$', cOrd),
    (r'^cadv\/$', cAdv),
    (r'^cdman\/$', cDman),
    (r'^user\/$', getUser),
    (r'^item\/$', getItemByKeyword),
)