#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from new31.cls import AjaxRJson
from functools import wraps
# Create your decorator here.

# 生产状态操作装饰器
def proDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from produce.models import Pro

        sn = int(kwargs['sn'])
        s = int(kwargs['s'])

        pro =  Pro.objects.get(id=sn)

        if s in Pro.objects.getActTuple(pro.status):

            return func(request, *args, **kwargs)

        else:

            return AjaxRJson().err( u'%s | %s - 无法%s' % (pro.ord.sn, pro.name, Pro.chcs[s][1]) )

    return _func