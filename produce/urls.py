# coding: UTF-8
from new31.func import pPatterns
from views import produce, nullPro, requirePro, duringPro, refusePro, readyPro

urlpatterns = pPatterns(
    (r'^$', produce, 3),
    (r'^(?P<s>0)\/(?P<sn>\d+)\/$', nullPro, 3),
    (r'^(?P<s>1)\/(?P<sn>\d+)\/$', requirePro, 3),
    (r'^(?P<s>2)\/(?P<sn>\d+)\/$', duringPro, 3),
    (r'^(?P<s>3)\/(?P<sn>\d+)\/$', refusePro, 3),
    (r'^(?P<s>4)\/(?P<sn>\d+)\/$', readyPro, 3)
)