#coding:utf-8
from django.http import HttpResponseRedirect
from models import *
from message.views import Message

# Create your views here.

class Purview:
    """权限处理类"""

    def __init__(self, request):
        self.request = request
        self.request.domElement = []
        self.request.s = self.request.user.is_authenticated() and self.request.user.is_staff

        p = []

        for i in Element.pPath:
            p.append(i[0])

        self.purview = tuple(p)


    def check(self):

        return self.isPurview()

    def isStaff(self,f):

        if self.request.user.is_authenticated() and self.request.user.is_staff :
            
            f(self.request)

        else:
            return self.redirectLogin()

    def isPurview(self):

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定

            if self.request.user.is_authenticated() and self.request.user.is_staff:

                try:
                    self.request.element = Element.objects.get(path=self.request.path)

                    return self.domElement() #页面元素权限加持

                except :
                    return self.msgPrint()

            else:
                return self.redirectLogin()


    def domElement(self):

        try:
            # 页面元素权限加持
            role = self.request.user.userrole.role

            if role.onLine:
                privilege = role.privilege

                if privilege.onLine:
                    domElement = privilege.element.get(path=self.request.path, onLine=True).sub_set.all()

                    for i in domElement:
                        try:
                            element = self.request.user.userrole.role.privilege.element.get(path=i.path)
                            if element.onLine:
                                self.request.domElement.append(element)
                        except:
                            pass

                else:
                    raise AttributeError

            else:
                raise AttributeError

            return None
        except:
            raise AttributeError

    def msgPrint(self):
        return Message(self.request).redirect(url=self.request.META.get('HTTP_REFERER',"/")).error('权限不足，无法进行当前操作。').officeMsg()

    def redirectLogin(self):
        return HttpResponseRedirect("/account/login/")