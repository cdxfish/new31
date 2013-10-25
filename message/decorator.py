#coding:utf-8
from functools import wraps
from models import Msg
from django.http import HttpResponse
# Create your decorator here.

# 信息验证装饰器
def readDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        for i in Msg.objects.filter(id__in=request.GET.getlist('id[]')):

            if i.user.id != request.user.id:

                return HttpResponse(Msg.objects.dumps(typ='error', msg=u'权限不足'))

        return func(request, *args, **kwargs)

    return _func

# 消息推送装饰器
def msgPushDr(func):
    @wraps(func)
    def __func(request, *args, **kwargs):
        Msg.objects.pushByPath(path=request.path, data={
                'sn': kwargs['sn'], 
                'from': u'%s%s' % (request.user.last_name, request.user.first_name)
            }, msg=u'%s' % func.__doc__)

        return func(request, *args, **kwargs)

    return __func

# 消息推送装饰器
def msgPushToRoleDr(*role):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            Msg.objects.pushToRole(*role, data={
                    'sn': kwargs['sn'], 
                    'from': u'%s%s' % (request.user.last_name, request.user.first_name)
                }, msg=u'%s' % func.__doc__)

            return func(request, *args, **kwargs)

        return __func
    return _func


# AJAX提错误提示示用
def ajaxErrMsg(msg):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)

            except:
                return HttpResponse(Msg.objects.dumps(msg=msg))
        return __func
    return _func