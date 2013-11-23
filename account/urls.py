#coding:utf-8
from new31.func import pPatterns
from views import login, logout, settings, saveSet, changepwd, cPwd, myOrd, uViewOrd, register, member, newUserFrm, userEditFrm

urlpatterns = pPatterns(
    (r'^$', myOrd, 2),
    (r'^login\/$', login, 2),
    (r'^logout\/$', logout, 2),
    (r'^settings\/$', settings, 2),
    (r'^sset\/$', saveSet, 2),
    (r'^changepwd\/$', changepwd, 2),
    (r'^cpwd\/$', cPwd, 2),
    (r'^view\/(?P<sn>\d{15})\/$', uViewOrd, 2),
    (r'^register\/$', register, 3),
    (r'^member\/$', member, 3),
    (r'^new\/$', newUserFrm, 3),
    (r'^edit\/(?P<u>[1][3|4|5|8][0-9]\d{8})\/$', userEditFrm, 3)
)