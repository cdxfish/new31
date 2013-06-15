#coding:utf-8
from django.http import HttpResponseRedirect
import math


# 格式化价格,舍弃小数位
def forMatFee(fee):

    return math.floor(fee)


# 重定向至登录页
def redirectLogin():
    return HttpResponseRedirect("/account/login/")


# 重定向至首页
def redirect():
    return HttpResponseRedirect('/')


# 重定向至前一页
def redirectBack(request):

    # if count() > 1:
    #     return redirect()
    # else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))


# 闭包计数器
def count(L=[]):

    L.append(1)
    
    return len(L)