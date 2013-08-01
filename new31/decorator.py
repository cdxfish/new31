#coding:utf-8
from django.contrib import messages
from django.http import HttpResponseRedirect
from new31.func import rdrtBck

# Create your decorator here.

# 提交模式检测包装函数
def postDr(func):
    def _func(request):
        if request.method == 'POST':
            return func(request)

        else:
            messages.error(request, '订单提交方式错误')

            return rdrtBck(request)
    return _func

# 提交模式检测包装函数
def postDrR(url):
    def _func(func):
        def __func(request):
            if request.method == 'POST':
                return func(request)

            else:
                messages.error(request, '订单提交方式错误')

                return HttpResponseRedirect(url)
        return __func
    return _func

# 页面跳转回上一页用装饰器
def rdrtBckDr(msg):
    def func(func):
        def _func(request):
            try:

                return func(request)
            except:
                messages.warning(request, msg)
                return rdrtBck(request)
        return _func
    return func