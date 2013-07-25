#coding:utf-8
from new31.func import *
from django.conf import settings
from django.contrib import messages

# Create your decorator here.

# 订单提交类提示用装饰器
def subMsg(s= ''):
    def _func(func):
        def __func(self):
            if not self.error:
                try:
                    return func(self)

                except Exception, e:
                    self.error = True
                    messages.error(self.request, s)
                    self.delNewOrd()

                    raise e

            return self #强制返回self否则无法链式调用
        return __func
    return _func


# AJAX提示用
def ajaxMsg(msg):
    def _func(func):
        def __func(request):
            try:
                return func(request)

            except:
                from ajax.views import AjaxRJson

                return AjaxRJson().message(msg).dumps()
        return __func
    return _func


# 提交模式检测包装函数
def postDr(func):
    def _func(request):
        if request.method == 'POST':
            return func(request)

        else:
            messages.error(request, '订单提交方式错误')

            return rdrtBck(request)
    return _func


# 页面跳转回上一页用装饰器
def rdrtBckDr(msg):
    def func(func):
        def _func(request):
            try:

                return func(request)
            except:

                return msg

            return rdrtBckDr()
        return _func
    return func

def itemonl(func):
    def _func(request):
        try:
            return func(request)
            
        except:
            messages.warning(request, '当前商品已下架')

            return rdrtBck(request)

    return _func


# 订单状态操作装饰器
def ordDetr(func):

    def _func(request, c):
        from order.models import Ord, OrdSats
        sn = request.GET.get('sn')
        order =  Ord.objects.get(sn=sn)
        act = OrdSats.objects.getActTuple(order.status)

        if not c in act:

            messages.error(request, u'%s - 无法%s' % (sn, OrdSats.chcs[c][1]))

            return rdrtBck(request)

        else:

            return func(request, c)

    return _func


# 物流状态操作装饰器
def shipDetr(func):
    def _func(request, c):
        from order.models import Ord, OrdShip
        sn = request.GET.get('sn')
        order =  Ord.objects.get(sn=sn)
        if not order.logcs.dman:
            messages.error(request, u'%s - 请选择物流师傅' % sn)

            return rdrtBck(request)


        act = OrdShip.objects.getActTuple(order.ordship.status)

        if not c in act:

            messages.error(request, u'%s - 无法%s' % (sn, OrdShip.chcs[c][1]))

            return rdrtBck(request)

        else:

            return func(request, c)

    return _func


# 生产状态操作装饰器
def proDetr(func):
    def _func(request, c):
        from produce.models import Pro
        sn = request.GET.get('sn')
        pro =  Pro.objects.get(item=sn)

        act = Pro.objects.getActTuple(pro.status)

        if not c in act:

            messages.error(request, u'%s | %s - 无法%s' % (pro.item.ord.sn, pro.item.name, Pro.chcs[c][1]))

            return rdrtBck(request)

        else:

            return func(request, c)

    return _func


# 支付状态操作装饰器
def fncDetr(func):
    def _func(request, c):
        from order.models import Ord, OrdFnc
        sn = request.GET.get('sn')
        pay =  Ord.objects.get(sn=sn).fnc

        act = OrdFnc.objects.getActTuple(pay.status)

        if not c in act:

            messages.error(request, u'%s - 无法%s' % (sn, OrdFnc.chcs[c][1]))

            return rdrtBck(request)

        else:

            return func(request, c)

    return _func