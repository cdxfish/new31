#coding:utf-8
from django.http import HttpResponseRedirect
from django.contrib import messages
from models import *
from new31.func import *

# Create your views here.

class Purview:
    """权限处理类"""

    def __init__(self, request):
        self.request = request
        self.request.domElement = []
        self.element = [] #用户可进入的页面权限集

        self.isStaff = self.self.request.user.is_authenticated() and self.request.user.is_staff

        self.purview = ( i[0] for i in Element.pPath )


    def check(self):

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定

            if self.isStaff:

                    if self.request.path in self.request.element:
                        self.domElement() #页面元素权限加持

                    else:
                        return self.error()

            else:
                return redirectLogin()


    # 页面元素加持
    def domElement(self):
        pass


    def error(self):
        messages.error(self.request, '权限不足，无法进行当前操作。')

        return redirectBack(self.request)
