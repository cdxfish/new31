#coding:utf-8
from new31.func import pPatterns
from views import printOrd

urlpatterns = pPatterns(
    (r'^$', printOrd, 3)
)