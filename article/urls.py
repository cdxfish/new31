# coding: UTF-8
from new31.func import pPatterns
from views import guide, about, ex, pub

urlpatterns = pPatterns(
    (r'^about\/$', about, 2),
    (r'^guide\/$', guide, 2),
    (r'^ex\/$', ex, 2),
    (r'^pub\/$', pub, 2)
)