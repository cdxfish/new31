#coding:utf-8
from django.http import HttpResponseRedirect
from django.contrib import messages
from models import *
from new31.func import *

# Create your views here.

class Purview:
    """ 后台全局安全控制类

        1. 根据后台url列表判定是否进行权限限制
        2. 根据当前url计算当前用户是否有进入权限
        3. 页面元素加持，用于基本信息显示


        判定方式:

        1. 是否需要判定
        2. 是否已登录
        3. 权限检查


    """

    def __init__(self, request):
        self.request = request
        self.request.domElement = [] #页面元素

        self.isStaff = self.request.user.is_authenticated() and self.request.user.is_staff #用户登录状态

        self.purview = ( i[0] for i in Element.pPath ) #需要判定的url列表
        self.request.paths = { v:i  for i, v in Element.pPath } #需要判定的url列表


    def check(self):

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定

            
            if self.request.user.is_authenticated() and self.request.user.is_staff:

                element =[]#用户可进入的页面权限集

                try:
                    self.domElement() #页面元素权限加持
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
        messages.error(self.request, u'权限不足。')

        return redirectBack(self.request)
