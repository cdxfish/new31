#coding:utf-8
u"""权限"""
from django.contrib import messages
from django.http import HttpResponse
from new31.func import rdrtBck, rdrtLogin
from django.core.urlresolvers import resolve, reverse
from message.models import Msg
import re
# Create your views here.

def purview(request):
    u"""权限"""

    return render_to_response('purviewui.htm', locals(), context_instance=RequestContext(request))


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
        self.request.domElement = resolve(self.request.path) #页面元素加持

        try:
            self.request.title = re.sub(r'.*: ', '', self.request.domElement.func.__doc__)
        except Exception, e:
            self.request.title = self.request.domElement.view_name

        self.isStaff = self.request.user.is_authenticated() and self.request.user.is_staff #用户登录状态

        self.purview = ( i[0] for i in Element.pPath ) #需要判定的url列表
        self.request.pPath = { i[1]:i[0] for i in Element.pPath } #需要判定的url列表
        self.request.nPath = { i[1]:i[0] for i in Element.nPath }

        for i in Element.pPath:
            if self.request.domElement.view_name in i:
                self.path = i

    def check(self):
        from models import Role, Element

        if self.request.domElement.view_name in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定
            if self.request.user.is_authenticated() and self.request.user.is_staff:

                try:
                    #用户可进入的页面权限集
                    if not self.request.domElement.view_name in Role.objects.getPathByUser(self.request.user): 
                        return self.error()

                    self.request.domElement.query = Element.objects.get(path=self.request.domElement.view_name)

                    self.request.domElement.sub_set = []
                    for i in self.request.domElement.query.sub_set.all():
                        _resolve = resolve(reverse(i.path))
                        try:
                            ituple = (i.path, re.sub(r'.*: ', '', _resolve.func.__doc__))
                        except Exception, e:
                            ituple = (i.path, i.get_path_display())

                        self.request.domElement.sub_set.append(ituple)

                except:
                    return self.error()

            else:
                return self.login()


    # 用户级错误提示
    def error(self):

        if self.path[2]:
            messages.error(self.request, self.errStr)

            return rdrtBck(self.request)

        else:
            from ajax.views import AjaxRJson
            return AjaxRJson().error(self.errStr)

    # 登录提示
    def login(self):
        if self.path[2]:
            return rdrtLogin(self.request)

        else:
            return HttpResponse(Msg.objects.dumps(typ='error', msg=u'请登录'))

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
        self.action = ()
        self.role = Role.objects.getPathByUser(request.user.id)

    def beMixed(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = []

            for ii in self.action[i.status]:
                try:
                    if ii[2] in self.role:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass


        return self

    def get(self):

        return self.beMixed().oList