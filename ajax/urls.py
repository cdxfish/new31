#coding:utf-8
from django.conf.urls import patterns
from new31.func import Patterns

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

# urlpatterns = Patterns(
#         (r'^itemmore\/$', getItemPin, 0, 0),
#         (r'^like\/$', itemLike, 0, 0),
#         (r'^itemspec\/$',getSpec, 0, 0),  #获取规格
#         (r'^cnum\/$', cNum, 0, 0),
#         (r'^clogcs\/$', cLogcs, 0, 0),
#         (r'^cfnc\/$', cFnc, 0, 0),
#         (r'^citem\/$', cItem, 0, 0),     
#         (r'^cord\/$', cOrd, 0, 1),
#         (r'^cadv\/$', cAdv, 0, 1),
#         (r'^cdman\/$', cDman, 0, 1),
#         (r'^user\/$', getUser, 0, 1),
#         (r'^item\/$', getItemByKeyword, 0, 1),
#     )