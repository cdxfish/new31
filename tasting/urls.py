# coding: UTF-8
from new31.func import pPatterns
from views import tasting, tastsave

urlpatterns = pPatterns(
    (r'^$', tasting, 2),
    (r'^tastsave\/$', tastsave, 2),
)