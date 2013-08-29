#coding:utf-8
from new31.func import pPatterns
from views import login, logout, settings, saveSet, changepwd, cPwd, myOrd, viewOrd

urlpatterns = pPatterns(
    (r'^$', myOrd, 'myOrd', 1, 0),
    (r'^login\/$', login, 1),
    (r'^logout\/$', logout),
    (r'^settings\/$', settings),
    (r'^sset\/$', saveSet),
    (r'^changepwd\/$', changepwd),
    (r'^cpwd\/$', cPwd),
    (r'^myord\/$', myOrd),
    (r'^view\/$', viewOrd),
)
