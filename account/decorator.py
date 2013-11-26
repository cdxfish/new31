#coding:utf-8
from django.contrib.auth.models import User
from django.contrib import messages
from new31.func import rdrtLogin, rdrtBck
from functools import wraps

# Create your decorator here.

# 登录验证装饰器
def loginDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        if request.user.is_active:
            
            return func(request, *args, **kwargs)
        else:
            return rdrtLogin(request, *args, **kwargs)

    return _func

# 会员查询装饰器, 用于检查会员是否存在
def checkUserDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        try:
            user = User.objects.get(username=kwargs['u'])
        except Exception, e:
            # raise e
            messages.error(request, u'[ %s ] 会员不存在' % kwargs['u'])

            return rdrtBck(request)

        else:
            return func(request, *args, **kwargs)
    return _func


# 会员信息验证装饰器, 用于检查会员的注册编辑等.
def uInfoDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from forms import NerUserFrm, BsInfoFrm, PtsFrm, EditUserFrm
        post = request.POST.dict()

        if post['u'] and post['u'] == post['username']:
            Frm = EditUserFrm
        else:
            Frm = NerUserFrm

        user = Frm({
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
            
            return func(request, *args, **kwargs)
        else:
            for i in user:
                if i.errors:
                    messages.error(request, u'%s - %s' % (i.label, i.errors))

            for i in bsinfo:
                if i.errors:
                    messages.error(request, u'%s - %s' % (i.label, i.errors))

            return rdrtBck(request)

    return _func

