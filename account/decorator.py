#coding:utf-8
from django.contrib import messages
from new31.func import rdrtLogin

# Create your decorator here.


# 订单提交类提示用装饰器
def loginDr(func):
    def _func(request):
        if request.user.is_active:
            
            return func(request)
        else:
            return rdrtLogin(request)

    return _func
