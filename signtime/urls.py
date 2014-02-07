# coding: UTF-8
from new31.func import pPatterns
from views import signtime

urlpatterns = pPatterns(
    (r'^$', signtime, 3)
)