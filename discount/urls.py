# coding: UTF-8
from new31.func import pPatterns
from views import dis

urlpatterns = pPatterns(
    (r'^$', dis, 3)
)