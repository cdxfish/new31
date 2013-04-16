#coding:utf-8
from django.http import HttpResponseRedirect
from account.views import UserInfo
from message.views import Message

# Create your views here.

class Purview:
    """权限处理类"""

    def __init__(self, request):
        self.request = request
        self.request.domElement = []
        self.request.s = self.request.user.is_authenticated() and self.request.user.is_staff

        self.purview = [
                          '/office/',
                          '/order/',
                          '/back/',
                          '/logistics/',
                          '/produce/',
                          '/inventory/',
                          '/after/',
                          '/tryeat/',
                          '/applytryeat/',
                          '/discount/',
                          '/ticket/',
                          '/integral/',
                          '/party/',
                          '/reconciliation/',
                          '/approved/',
                          '/reimburse/',
                          '/statistics/',
                          '/statssale/',
                          '/member/',
                          '/memberint/',
                          '/purview/',
                          '/adminlog/',
                          '/system/',
                          '/item/item/',
                          '/tag/tag/',
                          '/spec/',
                          '/price/',
                          '/slide/',
                          '/payment/',
                          '/area/',
                          '/signtime/',
                          '/logistics/',
                          '/area/',
                          '/filecheck/',
                        ] #权限对照用列表,用于识别那些页面需要进行权限判定

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
                    return self.domElement() #页面元素权限加持

                except :
                    return self.msgPrint()

            else:
                return self.redirectLogin()


    def domElement(self):

        try:
            # 页面元素权限加持
            role = self.request.user.userinfo.role

            if role.onLine:
                privilege = role.privilege

                if privilege.onLine:
                    domElement = privilege.element.get(path=self.request.path, onLine=True).sub_set.all()

                    for i in domElement:
                        try:
                            element = self.request.user.userinfo.role.privilege.element.get(path=i.path)
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
        return Message(self.request, self.request.META.get('HTTP_REFERER',"/")).autoRedirect(3). \
                title('错误').message('权限不足，无法进行当前操作。').officeMsg()

    def redirectLogin(self):
        return HttpResponseRedirect("/account/login/")