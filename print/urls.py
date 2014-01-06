# coding: UTF-8
from new31.func import pPatterns
from views import printOrd, pAct

urlpatterns = pPatterns(
    (r'^$', printOrd, 3),
    (r'^print\/(?P<sn>\d{15})\/$', pAct, 3)
)