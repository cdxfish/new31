#coding:utf-8
from django.http import HttpResponseRedirect
import math


# 格式化价格,舍弃小数位
def forMatFee(fee):

	return math.floor(fee)

# 重定向至登录页
def redirectLogin():
    return HttpResponseRedirect("/account/login/")


# 重定向至前一页
def redirectBack(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))