# coding: UTF-8
from django.http import HttpResponse
from django.contrib import messages
from new31.func import rdrtBck
from message.models import Msg
from functools import wraps
# Create your decorator here.

# 支付状态操作装饰器
def fncDetr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from finance.models import Fnc
        sn = int(kwargs['sn'])
        s = int(kwargs['s'])

        act = Fnc.objects.getActTuple(Fnc.objects.get(ord__sn=sn).status)

        if s in act:
            return func(request, *args, **kwargs)

        else:

            return HttpResponse(Msg.objects.dumps(typ='error', msg=u'%s - 无法%s' % (sn, Fnc.chcs[s][1]) ))

    return _func

# 支付方式信息检查装饰器
def chFncDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from forms import FncFrm
        from views import FncSess

        post = request.POST.dict() if len(request.POST.dict()) > 1 else FncSess(request).sess

        fncFrm = FncFrm(request)(post)

        if not fncFrm.is_valid():

            for i in fncFrm:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

            return rdrtBck(request)

        FncSess(request).setByDict(post)

        return func(request, *args, **kwargs)

    return _func

# 支付插件后续流程装饰器
def payFncDr(s):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            from finance.models import Fnc

            rf = func(request, *args, **kwargs)

            sn = int(kwargs['sn'])
            f = Fnc.objects.get(ord__sn=sn)

            if f.ord.user:
                try:
                    pt = f.ord.user.pts.pt
                    getattr(f.cod.main(f.ord, request), s)()
                except Exception, e:
                    return HttpResponse(Msg.objects.dumps(typ='error', msg=u'积分无法累积至帐户。'))
                else:
                    from log.models import AccountLog

                    note = u'订单流程: %d | 积分 %d > %d' % ( sn, pt, f.ord.user.pts.pt )

                    AccountLog.objects.update(f.ord.user, request.user, note)

            return rf

        return __func
    return _func