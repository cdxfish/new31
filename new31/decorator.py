# coding: UTF-8
from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from new31.func import rdrtBck
from functools import wraps
import time
# Create your decorator here.

# 提交模式检测包装函数
def postDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)

        else:
            messages.error(request, '提交方式错误')

            return rdrtBck(request)
    return _func

# 提交模式检测包装函数
def postDrR(name):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            if request.method == 'POST':
                return func(request, *args, **kwargs)

            else:
                messages.error(request, '提交方式错误')

                return redirect(name)
        return __func
    return _func

# 页面跳转回上一页用装饰器
def rdrtBckDr(msg):
    def func(func):
        @wraps(func)
        def _func(request, *args, **kwargs):
            try:

                return func(request, *args, **kwargs)
            except:
                messages.warning(request, msg)
                return rdrtBck(request)
        return _func
    return func

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        print 'start', start
        a = func(*args, **kwargs)
        end =time.clock()
        print 'end', end
        print 'used:', end - start

        return a
    return wrapper