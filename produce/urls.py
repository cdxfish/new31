#coding:utf-8
from new31.func import pPatterns
from views import produce, nullPro, requirePro, duringPro, refusePro, readyPro

urlpatterns = pPatterns(
    (r'^$', produce, 'produce', 3),
    (r'^0\/$', nullPro, 'nullPro', 3),
    (r'^1\/$', requirePro, 'requirePro', 3),
    (r'^2\/$', duringPro, 'duringPro', 3),
    (r'^3\/$', refusePro, 'refusePro', 3),
    (r'^4\/$', readyPro, 'readyPro', 3)
)