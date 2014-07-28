# coding: UTF-8
u"""备货"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import HttpResponse
from new31.func import rdrtBck
from new31.decorator import rdrtBckDr
from message.models import Msg
from message.decorator import ajaxErrMsg
from decorator import invNumDr
import datetime
# Create your views here.

def inventory(request):
    u"""备货"""
    from forms import InvSrchFrm
    from models import Build


    p = InvSrch(request)
    form = InvSrchFrm(initial=p.initial)

    a = form.initial

    invnum = p.get()

    invnum = InvPur(invnum, request).get()

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))

def stockInv(request):
    u"""备货清单"""
    from item.models import Item
    from models import Build, InvPro

    items = Item.objects.getAll()
    build = Build.objects.getByUser(request.user)

    for i in build:
        i.items = [{ 'name': ii.name, 'spec': [ {'id': spec.id, 'value': spec.spec.value, 'onl': InvPro.objects.hasPro(i.id, spec.id) } for spec in ii.itemspec_set.all() ]  } for ii in items]

    return render_to_response('inventorylist.htm', locals(), context_instance=RequestContext(request))

@ajaxErrMsg('该规格已下架')
def cOnlInv(request, sid, bid):
    u"""备货选择"""
    from models import InvPro

    return HttpResponse(Msg.objects.dumps(data={
                'onl': not InvPro.objects.cPro(bid=bid, sid=sid)
            }
        )
    )

def defaultInv(request, s):
    u"""备货格式化"""
    from models import InvNum, InvPro

    InvNum.objects.default(request.user, s)

    return rdrtBck(request)


def retMsg(inv):

    return HttpResponse(Msg.objects.dumps(data={
                'id': inv.id,
                'num': inv.num,
                'adv': inv.adv,
                'count': inv.count,
                'date': u'%s' % inv.date,
            }
        )
    )

@ajaxErrMsg('无法修改库存量')
@invNumDr
def minusInv(request, sid, num):
    u"""备货减"""
    from models import InvNum

    return retMsg(InvNum.objects.minus(sid, int(num)))


@ajaxErrMsg('无法修改库存量')
@invNumDr
def plusInv(request, sid, num):
    u"""备货加"""
    from models import InvNum

    return retMsg(InvNum.objects.plus(sid, int(num)))


class InvSrch(object):
    """
        备货基本搜索类

    """
    def __init__(self, request):


        self.request = request
        date = self.request.GET.get('s', '%s' % datetime.date.today())
        self.initial = {
                        's': date.strip(),
            }

    def get(self):
        from models import InvNum

        return InvNum.objects.getAll(self.initial['s']).filter(pro__build__area__name__in=[ i.area.name for i in self.request.user.attribution_set.all()]).distinct()


# 订单列表权限加持
from purview.views import BsPur
class InvPur(BsPur):
    """
        首先获取当前角色可进行的订单操作权限.

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        from models import InvNum

        super(InvPur, self).__init__(oList, request)

        self.action = InvNum.act


    def beMixed(self):

        for i in self.oList:
            i.sn = i.id
            if not hasattr(i,'action'):
                i.action = []

            for ii in self.action:
                try:
                    if ii[2] in self.role:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass

        return self