# coding: UTF-8
from new31.func import pPatterns
from views import shop, getItemPin

urlpatterns = pPatterns(
    (r'^$', shop, 2),
    (r'^itemmore\/$', getItemPin, 0)

)