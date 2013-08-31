#coding:utf-8
from new31.func import pPatterns
from views import search

urlpatterns = pPatterns(
    (r'^(?P<k>.*)\/$', search, 2)
)

