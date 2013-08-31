#coding:utf-8
from new31.func import pPatterns
from views import items

urlpatterns = pPatterns(
    (r'^item\/$', items, 3)
)