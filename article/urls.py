# coding: UTF-8
from new31.func import pPatterns
from views import article

urlpatterns = pPatterns(
    (r'^(?P<tag>.*)\/$', article, 2)
)