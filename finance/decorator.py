#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck

# Create your decorator here.


# 支付状态操作装饰器
def fncDetr(func):
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