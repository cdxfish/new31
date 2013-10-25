#coding:utf-8
from django.contrib import messages
from django.http import HttpResponse
from new31.func import rdrtBck
from message.models import Msg
from functools import wraps
# Create your decorator here.

# 生产状态操作装饰器
def proDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from produce.models import Pro

        sn = int(kwargs['sn'])
        s = int(kwargs['s'])

        p = Pro.objects.get(id=sn)

        if s in Pro.objects.getActTuple(p.status):

            return func(request, *args, **kwargs)

        else:

            return HttpResponse(Msg.objects.dumps(typ='error', msg= u'%s | %s - 当前状态无法%s' % (p.ord.sn, p.name, Pro.chcs[s][1]) ))

    return _func