#coding:utf-8
from new31.func import pPatterns
from views import newindex, newquery, newlogin, newcart

urlpatterns = pPatterns(
    (r'^$', newindex, 4),
    (r'^query\/$', newquery, 4),
    (r'^login\/$', newlogin, 4),
    (r'^cart\/$', newcart, 4)
)