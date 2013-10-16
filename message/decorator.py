#coding:utf-8
from functools import wraps
from new31.cls import AjaxRJson
# Create your decorator here.


# 信息验证装饰器
def readDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import Msg
        for i in Msg.objects.filter(id__in=request.GET.getlist('id[]')):

            if i.user.id != request.user.id:

                return AjaxRJson().err(u'权限不足')

        return func(request, *args, **kwargs)

    return _func
