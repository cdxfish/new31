#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps
# Create your decorator here.

# 生产状态操作装饰器
def proDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from produce.models import Pro

        pro =  Pro.objects.get(id=args[0])

        if args[1] in Pro.objects.getActTuple(pro.status):

            return func(request, *args, **kwargs)

        else:
            messages.error(request, u'%s | %s - 无法%s' % (pro.ord.sn, pro.name, Pro.chcs[args[1]][1]))

            return rdrtBck(request)

    return _func