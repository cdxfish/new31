# coding: UTF-8
from django.contrib import messages
from django.http import HttpResponse
from new31.func import rdrtBck
from message.models import Msg
from functools import wraps
# Create your decorator here.

# 试吃申请状态操作装饰器
def DiscussDr(func):
    @wraps(func)
    def __func(request, *args, **kwargs):
        from models import Discuss
        sn = kwargs['sn']
        s = int(kwargs['s'])

        di = Discuss.objects.get(id=sn)

        if request.user == di.user:

            return func(request, *args, **kwargs)
        else:

            return HttpResponse(Msg.objects.dumps(msg=u'%s - 无法%s' % (sn, Discuss.chcs[s][1])))

    return __func
