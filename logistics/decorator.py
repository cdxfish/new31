#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck

# Create your decorator here.

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

# 物流师傅必选装饰器
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
def aLogcsDr(func):
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