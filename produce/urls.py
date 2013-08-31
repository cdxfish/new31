#coding:utf-8
from new31.func import pPatterns
from views import produce, nullPro, requirePro, duringPro, refusePro, readyPro

urlpatterns = pPatterns(
    (r'^$', produce, 3),
    (r'^0\/$', nullPro, 3),
    (r'^1\/$', requirePro, 3),
    (r'^2\/$', duringPro, 3),
    (r'^3\/$', refusePro, 3),
    (r'^4\/$', readyPro, 3)
)