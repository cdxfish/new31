#coding:utf-8
from new31.func import pPatterns
from views import randomShow, tagShow, itemLike, getSpec

urlpatterns = pPatterns(
    (r'^$', randomShow, 2),
    (r'^like\/(?P<id>\d+)\/$', itemLike, 0),
    (r'^itemspec\/(?P<id>\d+)\/$', getSpec, 0),  #获取规格
    (r'^(?P<tag>.*)\/$', tagShow, 2)
)