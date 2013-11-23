#coding:utf-8
u"""用户中心"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from new31.func import rdrtLogin, rdrtBck, rdrtIndex, rdrtAcc
from new31.decorator import postDr
from decorator import loginDr
import re
# Create your views here.

def login(request):
    u"""用户登录"""

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

def newUserFrm(request):
    u"""新会员表单"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    uFrm = NerUserFrm()
    bsFrm = BsInfoFrm()
    pFrm = PtsFrm(initial={'pt':1000})

    return render_to_response('newuser.htm', locals(), context_instance=RequestContext(request))

def userEditFrm(request, u):
    u"""会员信息编辑表单"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    try:
        user = User.objects.get(username=u)
    except Exception, e:
        # raise e
        messages.error(request, u'[ %s ] 会员存在' % u)

        return rdrtBck(request)

    else:
        uFrm = NerUserFrm()
        bsFrm = BsInfoFrm()
        pFrm = PtsFrm(initial={'typ':0})

    return render_to_response('newuser.htm', locals(), context_instance=RequestContext(request))

@postDr
def register(request):
    u"""新会员表单提交"""
    from forms import NerUserFrm, BsInfoFrm, PtsFrm
    post = request.POST.dict()

    user = NerUserFrm({
                'username': post['username'],
                'last_name': post['last_name'],
                'first_name': post['first_name'],
            })

    bsinfo = BsInfoFrm({
                'sex': post['sex'],
                'mon': post['mon'],
                'day': post['day'],
                'typ': post['typ'],
            })

    pts = PtsFrm({
                'typ': post['typ']
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
    from forms import UserSrech

    _u = UserSrch(request)
    u = _u.get()

    form = UserSrech(initial=_u.initial)

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
            self.uList = self.uList.filter(username__regex=BsInfo.ure).filter(
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