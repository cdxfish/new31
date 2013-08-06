#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck

# Create your decorator here.

# 生产状态操作装饰器
def proDr(func):
    def _func(request, s):
        from produce.models import Pro

        id = request.GET.get('id')
        pro =  Pro.objects.get(id=id)

        act = Pro.objects.getActTuple(pro.status)

        if not s in act:

            messages.error(request, u'%s | %s - 无法%s' % (pro.ord.id, pro.name, Pro.chcs[s][1]))

            return rdrtBck(request)

        else:

            return func(request, s)

    return _func