# coding: UTF-8
from new31.func import pPatterns
from views import area

urlpatterns = pPatterns(
    (r'^$', area, 3)
)