#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages, auth
from new31.func import rdrtLogin, rdrtBck, rdrtIndex

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
    from order.models import Ord
    from produce.models import Pro

    ords = Ord.objects.getByUser(request.user.id)

    for i in ords:
        i.total = Pro.objects.getFeeBySN(i.sn)


    return render_to_response('myord.htm', locals(), context_instance=RequestContext(request))

def viewOrd(request):
    from order.models import Ord
    from produce.models import Pro

    sn = request.GET.get('sn')

    o = Ord.objects.get(sn=sn)

    if o.user != request.user:
        messages.error(request, u'您无法查看当前订单。')

        return rdrtBck(request)

    o.total = Pro.objects.getFeeBySN(sn)

    return render_to_response('vieword.htm', locals(), context_instance=RequestContext(request))


class UserInfo:

    def __init__(self, obj):
        self.obj = obj

    def newOrd(self):
        from order.models import Ord

        self.obj.newOrd = Ord.objects.lenNewOrd(self.obj.id)

        return self

    def newMsg(self):
        self.obj.newMsg = 0
        return self

    def allMsg(self):
        self.obj.allMsg = self.newOrd().obj.newOrd + self.newMsg().obj.newMsg

        return self

    def get(self):

        return self.newOrd().newMsg().allMsg().obj