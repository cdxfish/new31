# coding: UTF-8
from django.contrib import messages
from django.http import HttpResponse
from new31.func import rdrtBck
from functools import wraps
from message.models import Msg
# Create your decorator here.

# 物流状态操作装饰器
def logcsDr(typ=0):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            from models import Logcs
            sn = kwargs['sn']
            s = int(kwargs['s'])

            act = Logcs.objects.getActTuple(Logcs.objects.get(ord__sn=sn).status)

            if not s in act:
                if typ:

                    return HttpResponse(Msg.objects.dumps(typ='error', msg=u'%s - 无法%s' % (sn, Logcs.chcs[s][1]) ))
                else:
                    messages.error(request, u'%s - 无法%s' % (sn, Logcs.chcs[s][1]))

                    return rdrtBck(request)

            else:

                return func(request, *args, **kwargs)

        return __func
    return _func

# Ajax物流偏移量以及物流师傅选择装饰器
def aLogcsDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import Logcs

        sn = int(kwargs['sn'])

        logcs = Logcs.objects.get(ord=sn)

        if logcs.status > 1:
            return HttpResponse(Msg.objects.dumps(typ='error', msg=u'无法修改表单数据'))

        else:
            return func(request, *args, **kwargs)

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

        LogcSess(request).setByDict(post)

        return func(request, *args, **kwargs)

    return _func