#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.func import rdrtBck
from new31.decorator import rdrtBckDr
import datetime
# Create your views here.

def iUI(request):
    from forms import InvSrchFrm

    p = InvSrch(request)
    form = InvSrchFrm(initial=p.initial)

    a = form.initial

    pro = p.get()
    pro = InvPur(pro, request).get()
    pro = sort(pro)

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))

def sort(pro):
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


def iList(request):
    from item.models import Item

    items = Item.objects.getAll()

    return render_to_response('inventorylist.htm', locals(), context_instance=RequestContext(request))

@rdrtBckDr(u'该规格已下架')
def cOnl(request):
    from models import InvPro

    InvPro.objects.cOnl(int(request.GET.get('id')))

    return rdrtBck(request)

def default(request):
    from models import InvNum, InvPro

    InvNum.objects.default(InvSrch(request).initial['s'])

    return rdrtBck(request)

def minus(request):
    from models import InvNum
    InvNum.objects.minus(request.GET.get('id'))

    return rdrtBck(request)

def plus(request):
    from models import InvNum
    InvNum.objects.plus(request.GET.get('id'))

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
        self.path = request.paths[u'备货']

        self.chcs = InvPro.typ
        self.action = InvPro.act

    # 获取订单可选操作项
    def getElement(self):

        for i in self.oList:
            if not hasattr(i,'action'):
                i.action = {}

            i.action[self.path] = self.action[0]
            i.optr = 'id'
            i.value = i.invnum.id

        return self