#coding:utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.func import rdrtBck

# Create your decorator here.

# 订单状态操作装饰器
def ordDr(func):
    def _func(request, s):
        from order.models import Ord
        sn = request.GET.get('sn')
        order =  Ord.objects.get(sn=sn)

        act = Ord.objects.getActTuple(order.status)

        if not s in act:

            messages.error(request, u'%s - 无法%s' % (sn, Ord.chcs[s][1]))

            return rdrtBck(request)

        else:

            return func(request, s)

    return _func


# 订单提交类提示用装饰器(类内部使用)
def subMsg(s= ''):
    def _func(func):
        def __func(self):
            if not self.error:
                try:
                    return func(self)

                except Exception, e:
                    self.error = True
                    self.delNewOrd()
                    
                    messages.error(self.request, s)

            return self #强制返回self否则无法链式调用
        return __func
    return _func

# 订单提交类提示用装饰器
def subDr(func):
    def _func(request):

        try:
            return func(request)
        except Exception, e:
            return rdrtBck(request)

    return _func