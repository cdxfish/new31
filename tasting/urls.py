# coding: UTF-8
from new31.func import pPatterns
from views import tasting, tastsave, applys, note, notDis, acceptDis, refuseDis, doneDis

urlpatterns = pPatterns(
    (r'^$', tasting, 2),
    (r'^tastsave\/$', tastsave, 2),
    (r'^apply\/$', applys, 3),
    (r'^note\/(?P<sn>\d+)\/$', note, 1),
    (r'^(?P<s>0)\/(?P<sn>\d+)\/$', notDis, 1),
    (r'^(?P<s>1)\/(?P<sn>\d+)\/$', acceptDis, 1),
    (r'^(?P<s>2)\/(?P<sn>\d+)\/$', refuseDis, 1),
    (r'^(?P<s>3)\/(?P<sn>\d+)\/$', doneDis, 1)
)