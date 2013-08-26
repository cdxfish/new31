#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages, auth
from new31.func import rdrtLogin, rdrtBck, rdrtIndex, rdrtAcc
from decorator import loginDr

# Create your views here.

def login(request):
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

    auth.logout(request)

    return rdrtIndex()


@loginDr
def settings(request):
    from forms import setFrm
    frm = setFrm(request)

    return render_to_response('settings.htm', locals(), context_instance=RequestContext(request))

@loginDr
def saveSet(request):
    from models import BsInfo

    BsInfo.objects.set(request)

    return rdrtBck(request)


@loginDr
def changepwd(request):
    from django.contrib.auth.forms import PasswordChangeForm
    frm = PasswordChangeForm(request.user)


    return render_to_response('changepwd.htm', locals(), context_instance=RequestContext(request))


@loginDr
def cPwd(request):
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
    from order.models import Ord
    from produce.models import Pro

    ords = Ord.objects.getByUser(request.user.id)

    for i in ords:
        i.total = Pro.objects.getFeeBySN(i.sn)


    from models import UserData, BsInfo, Pts, UserPonints
    from django.contrib.auth.models import User

    users = UserData.objects.all()

    for i in users:
        try:

            u = User.objects.create_user(username=i.user_name, email=i.email, password='4000592731') 
            u.first_name = i.name[:1]
            u.last_name = i.name[1:] 
            u.is_active = True
            u.save()

            print '=' * 20
            print 'User', u.id, u.username, u.email, u.first_name, u.last_name, u.is_active

            d = i.birthday.split('-')

            b = BsInfo()
            b.user = u
            try:
                b.mon = d[0]
            except Exception, e:
                pass

            try:
                b.day = d[1]
            except Exception, e:
                pass

            b.sex = i.sex
            b.typ = i.register_type
            b.save()

            print 'BsInfo', b.id, b.user, b.mon, b.day, b.sex, b.typ

            up = UserPonints.objects.get(user_name=i.user_name)
            p = Pts()
            p.user = u
            p.pt = up.integral
            p.save()

            print 'Pts', p.id, p.user, p.pt
            print '=' * 20

        except Exception, e:
            pass



    # for i in User.objects.all():

    #     b = BsInfo()
    #     b.user = i

    #     b.save()

    #     p = Pts()
    #     p.user = i

    #     p.save()


    return render_to_response('myord.htm', locals(), context_instance=RequestContext(request))

@loginDr
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