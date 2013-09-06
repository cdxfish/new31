#coding:utf-8
u"""备货"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.func import rdrtBck
from new31.decorator import rdrtBckDr
import datetime
# Create your views here.

def inventory(request):
    u"""备货"""
    from forms import InvSrchFrm

    p = InvSrch(request)
    form = InvSrchFrm(initial=p.initial)

    a = form.initial

    pro = p.get()
    pro = InvPur(pro, request).get()
    pro = sort(pro)

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))

def sort(pro):
    u"""排序"""
    _pro = {}

    for i in pro:

        sn = i.spec.item.sn
        try:
            _pro[sn]['invnum'].append(i)
            _pro[sn]['adv'] += i.invnum.adv
            _pro[sn]['num'] += i.invnum.num
            _pro[sn]['count'] += i.invnum.count

        except Exception, e:
            _pro[sn] = {
                    'name': i.spec.item.name,
                    'invnum': [i, ],
                    'adv': i.invnum.adv,
                    'num': i.invnum.num,
                    'count': i.invnum.count,
                }

    return [v for i,v in _pro.items()]


def stockInv(request):
    u"""备货清单"""
    from item.models import Item

    items = Item.objects.getAll()

    return render_to_response('inventorylist.htm', locals(), context_instance=RequestContext(request))

@rdrtBckDr(u'该规格已下架')
def cOnlInv(request, sn):
    u"""备货选择"""
    from models import InvPro

    InvPro.objects.cOnl(sid=sn)

    return rdrtBck(request)

def defaultInv(request, s):
    u"""备货格式化"""
    from models import InvNum, InvPro

    InvNum.objects.default(s)

    return rdrtBck(request)

def minusInv(request, sn, num):
    u"""备货减"""
    from models import InvNum
    InvNum.objects.minus(sn, int(num))

    return rdrtBck(request)

def plusInv(request, sn, num):
    u"""备货加"""
    from models import InvNum
    InvNum.objects.plus(sn, int(num))

    return rdrtBck(request)


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

        return InvNum.objects.getAll(self.initial['s'])


# 订单列表权限加持
from purview.views import BsPur
class InvPur(BsPur):
    """
        首先获取当前角色可进行的订单操作权限. 

        其后获取订单的可选操作. 两者进行交集

    """
    def __init__(self, oList, request):
        from models import InvPro

        super(InvPur, self).__init__(oList, request)

        self.action = InvPro.act


    def beMixed(self):

        for i in self.oList:
            i.sn = i.id
            if not hasattr(i,'action'):
                i.action = []

            for ii in self.action[i.onl]:
                try:
                    if ii[2] in self.role:
                        i.action.append(ii)
                except Exception, e:
                    # raise e
                    pass

        return self