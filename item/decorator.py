#coding:utf-8
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps
# Create your decorator here.

# 商品下架装饰器
def itemonl(func):
	@wraps(func)
    def _func(request):
        try:
            return func(request)
            
        except:
            messages.warning(request, u'当前商品已下架')

            return rdrtBck(request)

    return _func