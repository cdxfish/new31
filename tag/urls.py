#coding:utf-8
from new31.func import pPatterns
from views import randomShow, tagShow

urlpatterns = pPatterns(
    (r'^$', randomShow, 2),
    (r'^(?P<tag>.*)\/$', tagShow, 2)
)