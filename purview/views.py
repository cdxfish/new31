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

        self.isStaff = self.request.user.is_authenticated() and self.request.user.is_staff

        self.purview = ( i[0] for i in Element.pPath )


    def check(self):

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定

            self.domElement() #页面元素权限加持
            
            if self.request.user.is_authenticated() and self.request.user.is_staff:

                element =[]#用户可进入的页面权限集

                try:
                    role = self.request.user.userrole.role
 
                    if role.onLine:
                        for i in role.privilege.filter(onLine=True):
                            for ii in i.element.filter(onLine=True):
                                element.append(ii.path)

                except:
                    return self.error()

                if not self.request.path in element:
                    return self.error()

            else:
                return redirectLogin()


    # 页面元素加持
    def domElement(self):
        self.request.domElement = Element.objects.getPath(path=self.request.path)

    # 用户级错误提示
    def error(self):
        messages.error(self.request, u'权限不足，无法进行 %s 操作。' % self.request.domElement.get_path_display())

        return redirectBack(self.request)
