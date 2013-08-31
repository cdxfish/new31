#coding:utf-8
u"""用户中心"""
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages, auth
from new31.func import rdrtLogin, rdrtBck, rdrtIndex, rdrtAcc
from decorator import loginDr

# Create your views here.

def login(request):
    u"""用户登录"""
    from django.contrib.auth.forms import AuthenticationForm

    # 避免重复登录
    if not request.user.is_authenticated():
        frm = AuthenticationForm(request)

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return rdrtAcc(request)
            else:
                # Show an error page

                messages.error(request, '用户名或密码错误')

                return rdrtLogin(request)

        else:
            return render_to_response('login.htm', locals(), context_instance=RequestContext(request))

    else:
        return rdrtAcc(request)

def logout(request):
    u"""用户登出"""

    auth.logout(request)

    return rdrtIndex()


@loginDr
def settings(request):
    u"""用户设置"""
    from forms import setFrm
    frm = setFrm(request)

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

@loginDr
def saveSet(request):
    u"""用户设置保存"""
    from models import BsInfo

    BsInfo.objects.set(request)

    return rdrtBck(request)


@loginDr
def changepwd(request):
    u"""用户密码修改"""
    from django.contrib.auth.forms import PasswordChangeForm
    frm = PasswordChangeForm(request.user)


    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))


@loginDr
def cPwd(request):
    u"""用户密码保存"""
    from django.contrib.auth.forms import PasswordChangeForm

    frm = PasswordChangeForm(user=request.user, data=request.POST)
    if frm.is_valid():
        frm.save()
        messages.success(request, u'密码修改成功。')
    else:
        for i in frm:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))

    return rdrtBck(request)


@loginDr
def myOrd(request):
    u"""我的订单"""
    from order.models import Ord
    from produce.models import Pro

    ords = Ord.objects.getByUser(request.user.id)

    for i in ords:
        i.total = Pro.objects.getFeeBySN(i.sn)


    return render_to_response('myord.htm', locals(), context_instance=RequestContext(request))

@loginDr
def uViewOrd(request, sn):
    u"""订单详情"""
    from order.models import Ord
    from produce.models import Pro

    o = Ord.objects.get(sn=sn)

    if o.user != request.user:
        messages.error(request, u'您无法查看当前订单。')

        return rdrtBck(request)

    o.total = Pro.objects.getFeeBySN(sn)

    return render_to_response('vieword.htm', locals(), context_instance=RequestContext(request))

def rUserd():
    u"""会员数据导入"""
    from models import uDATA, BsInfo, Pts
    from django.contrib.auth.models import User

    for i in uDATA.objects.all():
        u = User.objects.create_user(username=i.username, email=i.email, password='4000592731')

        u.first_name = i.first_name
        u.last_name = i.last_name
        u.is_active = True
        u.save()

        print '=' * 20
        print 'User', u.id, u.username, u.email, u.last_name, u.first_name, u.is_active
 
        b = BsInfo()
        b.user = u

        b.mon = i.mon

        b.day = i.day

        b.sex = i.sex
        b.typ = i.typ
        b.save()

        print 'BsInfo', b.id, b.user, b.mon, b.day, b.sex, b.typ

        p = Pts()

        p.pt = i.pt

        p.user = u

        p.save()

        print 'Pts', p.id, p.user, p.pt
        print '=' * 20