# coding: UTF-8
from django.http import HttpResponse
from message.models import Msg
from functools import wraps

# Create your decorator here.

# 库存量操作装饰器, 用于检查会员是否有权限进行操作
def invNumDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import InvNum

        InvNum.objects.get(id=kwargs['sid'])

        if not InvNum.objects.filter(id=kwargs['sid'], pro__build__area__name__in=request.user.attribution_set.getAreaList()):

            return HttpResponse(Msg.objects.dumps(typ='error', msg=u'无权限更改库存量'))

        else:

            return func(request, *args, **kwargs)

    return _func