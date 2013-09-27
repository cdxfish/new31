#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps
from new31.cls import AjaxRJson
# Create your decorator here.

# 物流状态操作装饰器
def logcsDr(typ=0):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            from models import Logcs

            act = Logcs.objects.getActTuple(Logcs.objects.get(ord__sn=args[0]).status)

            if not args[1] in act:
                if typ:

                    return AjaxRJson().err( u'%s - 无法%s' % (args[0], Logcs.chcs[args[1]][1]) )
                else:
                    messages.error(request, u'%s - 无法%s' % (args[0], Logcs.chcs[args[1]][1]))

                    return rdrtBck(request)

            else:

                return func(request, *args, **kwargs)

        return __func
    return _func


# 订单提交类提示用装饰器(类内部使用)
def modifyLogcsDr(i):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):

            return func(request, kwargs['sn'], i)

        return __func
    return _func


# 物流师傅必选装饰器
def dManDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import Logcs

        if not Logcs.objects.get(ord__sn=args[0]).dman:

            return AjaxRJson().err( u'请选择物流师傅')

        else:

            return func(request, *args, **kwargs)

    return _func 


# Ajax物流偏移量以及物流师傅选择装饰器
def aLogcsDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import Logcs
        from new31.cls import AjaxRJson

        
        sn = int(kwargs['sn'])
        value = int(kwargs['id'])

        logcs = Logcs.objects.get(ord=sn)

        if logcs.status > 1:
            return AjaxRJson().err(u'无法修改表单数据')

        func(logcs, value)

        logcs.save()

        return AjaxRJson().dumps({'sn': sn, 'value': value})

    return _func


# 物流信息检查装饰器
def chLogcsDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from forms import LogcsFrm
        from views import LogcSess

        post = request.POST.dict() if len(request.POST.dict()) > 1 else LogcSess(request).sess

        logcsFrm = LogcsFrm(post)

        if not logcsFrm.is_valid():

            for i in logcsFrm:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

            return rdrtBck(request)


        return func(request, *args, **kwargs)

    return _func