#coding:utf-8
from django.http import HttpResponseRedirect
from account.views import UserInfo

# Create your views here.

class Purview:
    """权限"""
    def check(self,request, appName):
        
        return self.isStaff(request, appName)

    def isStaff(self,request, appName):

        if request.user.is_authenticated() and request.user.is_staff :
            
            return self.isPurview(request, appName)

        else:
            return HttpResponseRedirect("/account/login/")

    def isPurview(self,request, appName):

        userPurview = UserInfo(request.user).purview().returnPurview()

        if request.path in userPurview:
            return appName(request)
        else:
            return HttpResponseRedirect("/account/login/")


class Ation:
    """docstring for Ation"""

    def action(self):

        return True