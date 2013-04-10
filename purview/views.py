#coding:utf-8
from django.http import HttpResponseRedirect
from account.views import UserInfo
from message.views import Message

# Create your views here.

class Purview:
    """权限处理类"""

    def __init__(self, request):
        self.request = request
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
        
        return self.isStaff()

    def isStaff(self):

        if self.request.user.is_authenticated() and self.request.user.is_staff :
            
            return self.isPurview()

        else:
            return HttpResponseRedirect("/account/login/")

    def isPurview(self):

        if self.request.path in self.purview: #进行权限页面对照,确认当前页面是否需要权限判定

            if not self.request.path in self.request.user.purview: #进行用户权限判定,确认当前用户是否有权进入该页面

                return Message(self.request, self.request.META.get('HTTP_REFERER',"/")).autoRedirect(3000). \
            title('错误').message('权限不足，无法进行当前操作。').officeMsg()


class Ation:
    """docstring for Ation"""

    def action(self):

        return True