#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages, auth
from new31.func import rdrtLogin, rdrtBck

# Create your views here.

def login(request):

    # 避免重复登录
    if not request.user.is_authenticated():
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return rdrtBck(request)
            else:
                # Show an error page

                messages.error(request, '用户名或密码错误')

                return rdrtLogin()

        else:
            return render_to_response('login.htm', locals(), context_instance=RequestContext(request))

    else:
        # 避免循环跳转
        if '/account/login/' in request.META.get('HTTP_REFERER', '/'):
            return rdrtIndex()
        else:
            return rdrtBck(request)

def logout(request):

    auth.logout(request)

    return rdrtIndex()

def settings(request):

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

def changepwd(request):

    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))

def myOrd(request):

    orders = Ord.objects.getOrdByUser(request.user.id)

    return render_to_response('myorder.htm', locals(), context_instance=RequestContext(request))

def orderDetail(request, orderSn):

    return render_to_response('orderdetail.htm', locals(), context_instance=RequestContext(request))


class UserInfo:

    def __init__(self, obj):
        self.obj = obj

    def newOrdCount(self):
        self.obj.newOrdCount = 2
        return self

    def newMsgCount(self):
        self.obj.newMsgCount = 1
        return self

    def allmsgCount(self):
        self.obj.allmsgCount = self.newOrdCount().obj.newOrdCount + self.newMsgCount().obj.newMsgCount

        return self


    def returnInfo(self):

        return self.obj