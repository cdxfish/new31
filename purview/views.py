#coding:utf-8
from django.http import HttpResponseRedirect
from django.contrib import messages
from new31.func import rdrtBck, rdrtLogin

# Create your views here.

class URLPurview:
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
        from models import Element

        self.errStr = u'权限不足。'
        self.request = request
        self.request.domElement = [] #页面元素

        self.isStaff = self.request.user.is_authenticated() and self.request.user.is_staff #用户登录状态

        self.purview = ( i[0] for i in Element.pPath ) #需要判定的url列表
        self.request.pPath = { v:i for i, v in Element.pPath } #需要判定的url列表
        self.request.nPath = { v:i for i, v in Element.nPath }


    def check(self):
        from models import Role

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定
            if self.request.user.is_authenticated() and self.request.user.is_staff:

                try:
                    self.domElement() #页面元素权限加持
                    element = Role.objects.getPathByUser(self.request.user) #用户可进入的页面权限集
                except:
                    return self.errorShow()

                if not self.request.path in element:
                    return self.error()
            else:
                return rdrtLogin(self.request)


    # 页面元素加持
    def domElement(self):
        from models import Element

        self.request.domElement = Element.objects.getPath(path=self.request.path)

        return self



    # 用户级错误提示
    def error(self):

        if self.request.domElement.typ:

            return self.errorShow()

        else: 
            from ajax.views import AjaxRJson
            return AjaxRJson().messages(self.errStr).dumps()

    def errorShow(self):
            messages.error(self.request, self.errStr)

            return rdrtBck(self.request)



class BsPur(object):
    """
        订单操作按钮元素级类

        主要用于显示各类对订单操作时的按钮显示


        原理为通过传入的订单.
        遍历订单的action属性.
        根据当前用户所具有的权限进行交集操作.

    """
    def __init__(self, oList, request):
        from order.models import Ord
        from models import Role
        self.oList = oList
        self.action = Ord.act
        self.role = Role.objects.getPathByUser(request.user)

    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[i.status]

        return self

    def beMixed(self):
        print self.role
        for i in self.oList:
            for ii in i.action:
                i.action[ii] = tuple([ iii for iii in i.action[ii] if u'%s%s/' % (ii, iii[0]) in self.role ])


        return self


    def mixedStatus(self):
        for i in self.oList:
            i.action[self.path] = tuple([ ii for ii in i.action[self.path] if ii in self.chcs ])

        return self


    def get(self):

        return self.getElement().beMixed().mixedStatus().oList