#coding:utf-8
from django.contrib import messages
from new31.func import rdrtLogin
from functools import wraps

# Create your decorator here.


# 登录验证装饰器
def loginDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        if request.user.is_active:
            
            return func(request, *args, **kwargs)
        else:
            return rdrtLogin(request, *args, **kwargs)

    return _func
