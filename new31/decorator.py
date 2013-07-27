#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck

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
                    self.delNewOrd()
                    
                    messages.error(self.request, s)

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
                messages.warning(request, msg)
                return rdrtBck(request)
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


# 物流状态操作装饰器
def logcsDr(func):
    def _func(request, s):
        from logistics.models import Logcs

        sn = request.GET.get('sn')

        act = Logcs.objects.getActTuple(Logcs.objects.get(ord__sn=sn).status)

        if not s in act:

            messages.error(request, u'%s - 无法%s' % (sn, Logcs.chcs[s][1]))

            return rdrtBck(request)

        else:

            return func(request, s)

    return _func

def dManDr(func):
    def _func(request, s):
        from logistics.models import Logcs

        sn = request.GET.get('sn')

        if not Logcs.objects.get(ord__sn=sn).dman:
            messages.error(request, u'%s - 请选择物流师傅' % sn)

            return rdrtBck(request)

        else:

            return func(request, s)

    return _func 

# Ajax物流偏移量以及物流师傅选择装饰器
def  aLogcsDr(func):
    def _func(request):
        from logistics.models import Logcs
        from ajax.views import AjaxRJson
        
        sn = int(request.GET.get('sn')[1:])
        value = int(request.GET.get('value', 0))

        logcs = Logcs.objects.get(ord=sn)

        if logcs.status > 1:
            return AjaxRJson.message(u'无法修改表单数据').dumps()

        func(logcs, value)

        logcs.save()

        return AjaxRJson().dumps({'sn': sn, 'value': value})

    return _func



# 生产状态操作装饰器
def proDr(func):
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