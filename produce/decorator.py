#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps
# Create your decorator here.

# 生产状态操作装饰器
def proDr(func):
    @wraps(func)
    def _func(request, s):
        from produce.models import Pro

        id = request.GET.get('id')
        pro =  Pro.objects.get(id=id)

        # if s in Pro.objects.getActTuple(pro.status) and pro.ord.isConfrm():
        if s in Pro.objects.getActTuple(pro.status):

            return func(request, s)

        else:
            messages.error(request, u'%s | %s - 无法%s' % (pro.ord.sn, pro.name, Pro.chcs[s][1]))

            return rdrtBck(request)

    return _func