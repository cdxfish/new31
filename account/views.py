#coding:utf-8
u"""用户中心"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages, auth
from new31.func import rdrtLogin, rdrtBck, rdrtIndex, rdrtAcc
from new31.decorator import postDr
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
    from forms import bsInfoFrm
    frm = bsInfoFrm(request)

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

@postDr
def register(request):
    u"""新会员表单提交"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    post = request.POST.dict()

    user = NerUserFrm({
                'username': post[u'username'],
                'last_name': post[u'last_name'],
                'first_name': post[u'first_name'],
            })

    bsinfo = BsInfoFrm({
                'sex': post[u'sex'],
                'mon': post[u'mon'],
                'day': post[u'day'],
                'typ': post[u'typ'],
            })

    pts = PtsFrm({
                'typ': post[u'typ']
            })

    if user.is_valid() and bsinfo.is_valid():
        from models import BsInfo

        BsInfo().newUser(post)
    else:
        for i in user:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))

        for i in bsinfo:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))

        return HttpResponseRedirect(reverse('account:newUserFrm'))

    return HttpResponseRedirect(u'%s?k=%s' % (reverse('account:member'), post[u'username']))

def member(request):
    u"""会员信息"""
    k = request.GET.get('k', '')
    u = User.objects.filter(username__contains=k).order_by('-id')[:100]

    return render_to_response('member.htm', locals(), context_instance=RequestContext(request))

def newUserFrm(request):
    u"""新会员表单"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    user = NerUserFrm()
    bsinfo = BsInfoFrm()
    pts = PtsFrm(initial={'typ':0})

    return render_to_response('newuser.htm', locals(), context_instance=RequestContext(request))

def integral(request, sn):
    u"""会员积分"""
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