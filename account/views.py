# coding: UTF-8
u"""用户中心"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.db.models import Q
from new31.func import rdrtBck
from new31.decorator import postDr
from forms import QuicklyNewUserFrm
from decorator import uInfoDr, checkUserDr, userLogDr, checkOrdByUserDr
import re
# Create your views here.

def login(request):
    u"""用户登录"""
    # 避免重复登录
    if not request.user.is_authenticated():
        if request.method == 'GET':
            nfrm = UserCreationForm()
            frm = AuthenticationForm(request)
            next = request.GET.get('next', 'account:myOrd')

            return render_to_response('login.htm', locals(), context_instance=RequestContext(request))

        elif request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            next = request.POST.get('next', 'account:myOrd')

            user = auth.authenticate(username=username, password=password)

            if user and user.is_active:
                # Correct password, and the user is marked "active"
                auth.login(request, user)
                # Redirect to a success page.
                return redirect(next)
            else:
                # Show an error page
                messages.error(request, '用户名或密码错误')

                return redirect(request.META.get('HTTP_REFERER', 'shop:shop'))
    else:
        return redirect('account:myOrd')

@postDr
def quicklyREG(request):
    u"""快速注册"""
    form = QuicklyNewUserFrm(request.POST)
    if form.is_valid():
        new_user = form.save()

        return redirect('account:settings')
    else:
        for i in form:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))
        return redirect('account:login')

def logout(request):
    u"""用户登出"""

    auth.logout(request)

    return redirect('account:login')


@login_required
def settings(request):
    u"""个人信息"""
    from forms import bsInfoFrm
    frm = bsInfoFrm(request)

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

@login_required
def saveSet(request):
    u"""用户设置保存"""
    from models import BsInfo

    BsInfo.objects.set(request)

    return rdrtBck(request)


@login_required
def changepwd(request):
    u"""用户密码修改"""
    from django.contrib.auth.forms import PasswordChangeForm
    frm = PasswordChangeForm(request.user)

    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))


@login_required
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


@login_required
def myOrd(request):
    u"""我的订单"""
    from order.models import Ord
    from produce.models import Pro

    ords = Ord.objects.getByUser(request.user.id)

    return render_to_response('myord.htm', locals(), context_instance=RequestContext(request))

@login_required
@checkOrdByUserDr
def uViewOrd(request, sn):
    u"""订单详情"""
    from order.models import Ord

    o = Ord.objects.get(sn=sn)
    o.pay = o.fnc.cod.main(o, request)

    return render_to_response('vieword.htm', locals(), context_instance=RequestContext(request))

def newUserFrm(request):
    u"""新会员表单"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    uFrm = NerUserFrm()
    bsFrm = BsInfoFrm()
    pFrm = PtsFrm(initial={'pt':0})

    return render_to_response('newuser.htm', locals(), context_instance=RequestContext(request))

@postDr
@uInfoDr
def register(request):
    u"""新会员表单提交"""
    from models import BsInfo

    post = request.POST.dict()

    BsInfo().newUser(post)

    return redirect(u'%s?k=%s' % (reverse('account:member'), post[u'username']))

@checkUserDr
def userEditFrm(request, u):
    u"""会员信息编辑表单"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm

    u = User.objects.get(username=u)
    uFrm = NerUserFrm(initial={
        'username': u.username,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'email': u.email
        })
    bsFrm = BsInfoFrm(initial={
        'sex': u.bsinfo.sex,
        'mon': u.bsinfo.mon,
        'day': u.bsinfo.day,
        'typ': u.bsinfo.typ,
        })
    pFrm = PtsFrm(initial={'pt':u.pts.pt})

    return render_to_response('newuser.htm', locals(), context_instance=RequestContext(request))

@postDr
@uInfoDr
@userLogDr
def userEdit(request):
    u"""会员信息编辑提交"""
    from models import BsInfo

    post = request.POST.dict()

    BsInfo().editUser(post)
    return redirect(u'%s?k=%s' % (reverse('account:member'), post[u'username']))


def member(request):
    u"""会员信息"""
    from forms import UserSrechFrm

    _u = UserSrch(request)
    u = _u.get()

    form = UserSrechFrm(initial=_u.initial)

    return render_to_response('member.htm', locals(), context_instance=RequestContext(request))



class UserSrch(object):
    """
        订单基本搜索类

    """
    def __init__(self, request):
        self.request = request

        self.uList = User.objects.select_related().all()
        self.initial = {
                        'k': request.GET.get('k', '').strip(),
            }


    def baseSearch(self):
        from models import BsInfo
        if re.match(ur'\d{2}\-\d{2}', self.initial['k']):
            self.uList = self.uList.filter(bsinfo__mon=int(self.initial['k'][:2]), bsinfo__day=int(self.initial['k'][3:]))
        else:
            self.uList = self.uList.filter(is_staff=False).filter(
                    Q(username__contains=self.initial['k']) |
                    Q(first_name__contains=self.initial['k']) |
                    Q(last_name__contains=self.initial['k'])
                ).order_by('-id')

        return self

    def search(self):

        return self


    def page(self):
        from new31.func import page

        return page(l=self.uList, p=int(self.request.GET.get('p', 1)))

    def get(self):

        return self.baseSearch().search().page()