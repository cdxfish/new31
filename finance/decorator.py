#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps
# Create your decorator here.


# 支付状态操作装饰器
def fncDetr(func):
    @wraps(func)
    def _func(request, s):
        from finance.models import Fnc
        sn = request.GET.get('sn')

        act = Fnc.objects.getActTuple(Fnc.objects.get(ord=sn).status)

        if not s in act:

            messages.error(request, u'%s - 无法%s' % (sn, Fnc.chcs[s][1]))

            return rdrtBck(request)

        else:

            return func(request, s)

    return _func



# 支付方式信息检查装饰器
def chFncDr(func):
    @wraps(func)
    def _func(request):
        from forms import FncFrm
        from views import FncSess

        post = request.POST.dict() if len(request.POST.dict()) > 1 else FncSess(request).sess

        fncFrm = FncFrm(post)

        if not fncFrm.is_valid():

            for i in fncFrm:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

            return rdrtBck(request)

        return func(request)

    return _func
