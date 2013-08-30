#coding:utf-8
from new31.func import pPatterns
from views import spec

urlpatterns = pPatterns(
    (r'^$', spec, 'spec', 3)
)