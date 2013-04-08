#coding:utf-8
from django.http import HttpResponseRedirect
from account.views import UserInfo
from message.views import Message

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

        if request.path in request.user.purview:
            return appName(request)
        else:
            return Message(request, request.META.get('HTTP_REFERER',"/")).autoRedirect(3). \
        title('错误').message('权限不足，无法查看当前页面。').officeMsg()


class Ation:
    """docstring for Ation"""

    def action(self):

        return True