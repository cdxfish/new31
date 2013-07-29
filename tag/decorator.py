#coding:utf-8
from django.contrib import messages

# Create your decorator here.

# 错误标签提示装饰器
def noTagDr(func):
    def _func(self, tag):
        try:
            return func(self, tag)
        except:
            messages.warning(self.request, '此标签不存在。')

    return _func