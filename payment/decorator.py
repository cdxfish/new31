#coding:utf-8
from django.contrib.auth.models import User
from django.contrib import messages
from new31.func import rdrtBck
from functools import wraps

# Create your decorator here.

# 表单验证装饰器
def frmDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from models import Pay
        from forms import PayFrm

        pay = Pay.objects.get(id=request.POST.get('id'))

        frm = PayFrm(pay)(request.POST.dict())

        if frm.is_valid():
            return func(request, *args, **kwargs)

        else:
            for i in frm:
                if i.errors:
                    messages.error(request, u'%s - %s' % (i.label, i.errors))

            return rdrtBck(request)
    return _func