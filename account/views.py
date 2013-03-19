#coding:utf-8
from django.shortcuts import render_to_response
from django.contrib import auth
from django.template import RequestContext
from django.http import HttpResponseRedirect
from message.views import *
from account.models import *

# Create your views here.

def login(request):

    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect("/")
            else:
                # Show an error page
                return Message(request.META.get('HTTP_REFERER',"/")).autoRedirect().title('错误').message('用户名或密码错误!').printMsg()

        else:
            return render_to_response('login.htm', locals(), context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect("/")

def logout(request):

    auth.logout(request)

    return HttpResponseRedirect("/")

def settings(request):

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

def changepwd(request):

    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))

def myOrder(request):

    return render_to_response('myorder.htm', locals(), context_instance=RequestContext(request))

def orderDetail(request, orderSn):

    return render_to_response('orderdetail.htm', locals(), context_instance=RequestContext(request))


class UserInfo:

    def __init__(self, obj):
        self.obj = obj

    def newOrderCount(self):
        self.obj.newOrderCount = 2
        return self

    def newMsgCount(self):
        self.obj.newMsgCount = 1
        return self

    def allmsgCount(self):
        self.obj.allmsgCount = self.newOrderCount().obj.newOrderCount + self.newMsgCount().obj.newMsgCount

        return self

    def purview(self):
        self.obj.purview = [
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
                          '/item/admin/',
                          '/tag/admin/',
                          '/specification/',
                          '/price/',
                          '/slide/',
                          '/payment/',
                          '/area/',
                          '/signtime/',
                          '/logistics/',
                          '/area/',
                          '/filecheck/',
                        ]

        return self

    def returnPurview(self):

        return self.obj.purview
        # return dict.fromkeys(self.obj.purview,True) 

    def returnInfo(self):

        return self.obj