#coding:utf-8
from new31.func import pPatterns
from views import log

urlpatterns = pPatterns(
    (r'^$', log, 3)
)   