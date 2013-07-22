#coding:utf-8
from new31.func import *
from django.conf import settings
from django.contrib import messages

# Create your decorator here.

# 订单提交类提示用装饰器
def subFailRemind(s= ''):
    def _newfunc(func):
        def __newfunc(self):
            if not self.error:
                try:
                    return func(self)

                except Exception, e:
                    self.error = True

                    messages.error(self.request, s)
                    if settings.DEBUG:
                        self.delNewOrd()
                        raise e

            return self #强制返回self否则无法链式调用
        return __newfunc
    return _newfunc


# AJAX提示用
def errMsg(msg):

    def _errMsg(func):

        def __errMsg(request, **kwargs):
            try:

                return func(request, kwargs)
            except:
                from ajax.views import AjaxRJson

                return AjaxRJson().message(msg).dumps()

        return __errMsg

    return _errMsg


# 提交模式检测包装函数
def checkPOST(func):
    def _func(request):
        if request.method == 'POST':

            return func(request)

        else:

            messages.error(request, '订单提交方式错误')

            return rdrBck(request)

    return _func



# 页面跳转提示用装饰器
def redirMsg(msg):

    def _redirMsg(func):

        def __redirMsg(request, **kwargs):
            if settings.DEBUG:

                return func(request, kwargs)

            else:
                try:

                    return func(request, kwargs)
                except:

                    return msg

        return __redirMsg

    return _redirMsg


# 页面跳转回上一页用装饰器
def rdrBckDr(func):

    def _func(request, **kwargs):
        
        func(request, kwargs)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER',"/"))

    return _func


# 根据settings.DEBUG设置是否显示用户级提示信息
def itemonl(func):

    def _func(request, kwargs):

        if settings.DEBUG:

            return func(request, kwargs)

        else:
            try:

                return func(request, kwargs)
                
            except:

                messages.warning(request, '当前商品已下架')

                return rdrBck(request)

    return _func


# 订单状态操作装饰器
def conOrd(func):

    def _func(request, c):
        from order.models import OrdInfo, OrdSats
        sn = request.GET.get('sn')
        order =  OrdInfo.objects.get(sn=sn).ordsats
        act = OrdSats.objects.getActTuple(order.status)

        if not c in act:

            messages.error(request, u'%s - 无法%s' % (sn, OrdSats.chcs[c][1]))

            return rdrBck(request)

        else:

            return func(request, c)

    return _func


# 物流状态操作装饰器
def conShip(func):
    def _func(request, c):
        from order.models import OrdInfo, OrdShip
        sn = request.GET.get('sn')
        order =  OrdInfo.objects.get(sn=sn)
        if not order.ordlogcs.dman:
            messages.error(request, u'%s - 请选择物流师傅' % sn)

            return rdrBck(request)


        act = OrdShip.objects.getActTuple(order.ordship.status)

        if not c in act:

            messages.error(request, u'%s - 无法%s' % (sn, OrdShip.chcs[c][1]))

            return rdrBck(request)

        else:

            return func(request, c)

    return _func