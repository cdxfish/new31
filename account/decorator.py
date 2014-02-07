# coding: UTF-8
from django.contrib.auth.models import User
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps

# Create your decorator here.

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

        if post.get('u') and post.get('u') == post['username']:
            Frm = EditUserFrm
        else:
            Frm = NerUserFrm

        user = Frm({
                    'username': post['username'],
                    'last_name': post['last_name'],
                    'first_name': post['first_name'],
                    'email': post['email'],
                })

        bsinfo = BsInfoFrm({
                    'sex': post['sex'],
                    'mon': post['mon'],
                    'day': post['day'],
                    'typ': post['typ'],
                })

        pts = PtsFrm({
                    'pt': post['pt']
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

def userLogDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from log.models import AccountLog
        try:
            u = User.objects.get(username=request.POST.get('u'))

            rObj = func(request, *args, **kwargs)

            _u = User.objects.get(username=request.POST.get('username'))

            edit = 'edit: '

            edit += '[%s %s > %s] ' % (u'用户名', u.username, _u.username)
            edit += '[%s %s > %s] ' % (u'姓氏', u.last_name, _u.last_name)
            edit += '[%s %s > %s] ' % (u'名字', u.first_name, _u.first_name)
            edit += '[%s %s > %s] ' % (u'电子邮件地址', u.email, _u.email)
            edit += '[%s %s > %s] ' % (u'性别', u.bsinfo.get_sex_display(), _u.bsinfo.get_sex_display())
            edit += '[%s %s > %s] ' % (u'月', u.bsinfo.get_mon_display(), _u.bsinfo.get_mon_display())
            edit += '[%s %s > %s] ' % (u'日', u.bsinfo.get_day_display(), _u.bsinfo.get_day_display())
            edit += '[%s %s > %s] ' % (u'类型', u.bsinfo.get_typ_display(), _u.bsinfo.get_typ_display())
            edit += '[%s %s > %s] ' % (u'积分', u.pts.pt, _u.pts.pt)

            a = AccountLog()
            a.user = _u
            a.act = request.user
            a.note = edit
            a.save()


        except Exception, e:
            # raise e
            messages.error(request, u'无法写入会员日志')

            return rdrtBck(request)
        finally:

            return rObj

    return _func

# 订单所属检查装饰器, 用于检查订单是否属于当前会员
def checkOrdByUserDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from order.models import Ord
        try:
            o = Ord.objects.get(sn=kwargs['sn'])
        except Exception, e:
            # raise e
            messages.error(request, u'订单不存在。')
            return rdrtBck(request)
        else:
            if o.user != request.user:
                messages.error(request, u'您无法查看当前订单。')

                return rdrtBck(request)
            else:
                return func(request, *args, **kwargs)
    return _func