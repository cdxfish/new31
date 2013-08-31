#coding:utf-8
from new31.func import pPatterns
from views import bom

urlpatterns = pPatterns(
    (r'^$', bom, 3)
)