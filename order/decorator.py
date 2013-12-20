#coding:utf-8
from django.contrib import messages
from django.http import HttpResponse
from new31.func import rdrtBck
from message.models import Msg
from functools import wraps
# Create your decorator here.

# 订单状态操作装饰器
def ordDr(typ=0):
    def _func(func):
        @wraps(func)
        def __func(request, *args, **kwargs):
            from order.models import Ord
            sn = kwargs['sn']
            s = int(kwargs['s'])
            order =  Ord.objects.get(sn=sn)

            if not s in Ord.objects.getActTuple(order.status):

                if typ:

                    return HttpResponse(Msg.objects.dumps(msg=u'%s - 无法%s' % (sn, Ord.chcs[s][1])))
                else:
                    messages.error(request, u'%s - 无法%s' % (sn, Ord.chcs[s][1]))

                    return rdrtBck(request)

            else:

                return func(request, *args, **kwargs)

        return __func
    return _func


# 订单提交类提示用装饰器(类内部使用)
def subMsg(s= ''):
    def _func(func):
        @wraps(func)
        def __func(self, *args, **kwargs):
            if not self.error:
                try:
                    return func(self, *args, **kwargs)

                except Exception, e:
                    self.error = True
                    self.delNewOrd()

                    messages.error(self.request, s)
                    raise e # 如需debug这取消此注释


            return self #强制返回self否则无法链式调用
        return __func
    return _func

# 订单提交类提示用装饰器
def subDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):

        try:
            return func(request, *args, **kwargs)
        except Exception, e:

            raise e # 如需debug这取消此注释
            return rdrtBck(request)

    return _func

# 订单提交基本信息监测装饰器
def ordSubDr(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        from forms import OrdFrm
        from views import OrdSess
        from models import Ord

        post = request.POST.dict() if len(request.POST.dict()) > 1 else OrdSess(request).sess

        ordFrm = OrdFrm(post)

        if not ordFrm.is_valid():

            for i in ordFrm:
                if i.errors:

                    messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

            return rdrtBck(request)

        sn = int(post['sn'])
        if sn:
            order = Ord.objects.get(sn=sn)
            if Ord._chcs[1][0] in Ord.objects.getActTuple(order.status):

                OrdSess(request).setOrdToEdit(sn)
            else:
                messages.warning(request, '%d - %s' % ( sn, u'当前订单不可编辑.'))

                return rdrtBck(request)

        else:
            OrdSess(request).setOrdtoNew()

        return func(request, *args, **kwargs)

    return _func