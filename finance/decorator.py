#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from new31.cls import AjaxRJson
from functools import wraps
# Create your decorator here.


# 支付状态操作装饰器
def fncDetr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from finance.models import Fnc

        act = Fnc.objects.getActTuple(Fnc.objects.get(ord=args[0]).status)

        if args[1] in act:
            return func(request, *args, **kwargs)

        else:

            return AjaxRJson().err( u'%s - 无法%s' % (args[0], Fnc.chcs[args[1]][1]) )

    return _func

# 支付方式信息检查装饰器
def chFncDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from forms import FncFrm
        from views import FncSess

        post = request.POST.dict() if len(request.POST.dict()) > 1 else FncSess(request).sess

        fncFrm = FncFrm(post)

        if not fncFrm.is_valid():

            for i in fncFrm:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

            return rdrtBck(request)

        return func(request, *args, **kwargs)

    return _func
