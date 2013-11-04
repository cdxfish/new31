#coding:utf-8
from new31.func import pPatterns
from views import newindex, newquery

urlpatterns = pPatterns(
    (r'^$', newindex, 4),
    (r'^query\/$', newquery, 4)
)