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
    # def make_adder():
    #     i = 0
    #     def adder():
    #         return i =+ 1
    #     return adder
    import sys
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print sys.getrefcount(redirectBack)
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'
    print '---------------------------'

    if sys.getrefcount(redirectBack) > 1:
        return redirect()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))