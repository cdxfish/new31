#coding:utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.func import rdrtBck
from new31.cls import AjaxRJson
from functools import wraps
# Create your decorator here.

# 订单状态操作装饰器
def ordDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from order.models import Ord
        sn = args[0]
        order =  Ord.objects.get(sn=sn)

        if not args[1] in Ord.objects.getActTuple(order.status):

            messages.error(request, u'%s - 无法%s' % (sn, Ord.chcs[args[1]][1]))

            return rdrtBck(request)

        else:

            return func(request, *args, **kwargs)

    return _func

def ajaxOrdDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from order.models import Ord
        order =  Ord.objects.get(sn=args[0])

        if not args[1] in Ord.objects.getActTuple(order.status):

            return AjaxRJson().err( u'%s - 无法%s' % (args[0], Ord.chcs[args[1]][1]) )

        else:

            return func(request, *args, **kwargs)

    return _func


# 订单提交类提示用装饰器(类内部使用)
def modifyDr(i):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):

            return func(request, kwargs['sn'], i)

        return __func
    return _func


# 订单提交类提示用装饰器(类内部使用)
def subMsg(s= ''):
    def _func(func):
        @wraps(func)
        def __func(self, *args, **kwargs):
            if not self.error:
                try:
                    return func(self, *args, **kwargs)

                except Exception, e:
                    self.error = True
                    self.delNewOrd()
                    
                    messages.error(self.request, s)

            return self #强制返回self否则无法链式调用
        return __func
    return _func

# 订单提交类提示用装饰器
def subDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):

        try:
            return func(request, *args, **kwargs)
        except Exception, e:
            return rdrtBck(request)

    return _func