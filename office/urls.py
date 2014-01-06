# coding: UTF-8
from new31.func import pPatterns
from views import office

urlpatterns = pPatterns(
    (r'^$', office, 3)
)