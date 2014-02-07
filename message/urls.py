# coding: UTF-8
from new31.func import pPatterns
from views import get, read

urlpatterns = pPatterns(
    (r'^get\/$', get, 1),
    (r'^read\/$', read, 1)
)