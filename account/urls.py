#coding:utf-8
from new31.func import pPatterns
from views import login, logout, settings, saveSet, changepwd, cPwd, myOrd, viewOrd

urlpatterns = pPatterns(
    (r'^$', myOrd, 'myOrd', 2),
    (r'^login\/$', login, 'login', 2),
    (r'^logout\/$', logout, 'logout', 2),
    (r'^settings\/$', settings, 'userSet', 2),
    (r'^sset\/$', saveSet, 'userSetSave', 2),
    (r'^changepwd\/$', changepwd, 'changepwd', 2),
    (r'^cpwd\/$', cPwd, 'cPwd', 2),
    (r'^view\/$', viewOrd, 'UserViewOrd', 2)
)
