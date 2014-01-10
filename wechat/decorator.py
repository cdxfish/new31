#coding:utf-8
from functools import wraps
# Create your decorator here.

# 订单日志装饰器
def ordLogDr(func):
    @wraps(func)
    def __func(request, *args, **kwargs):
        from order.models import Ord
        from models import OrdLog

        OrdLog.objects.saveLog(Ord.objects.get(sn=kwargs['sn']), request)

        return func(request, *args, **kwargs)

    return __func