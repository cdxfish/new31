# coding: UTF-8
u"""购物车"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from decorator import itemshow, checkCartDr
from order.decorator import subDr
from new31.func import f02f
from new31.decorator import postDrR
from message.models import Msg
from message.decorator import ajaxErrMsg
from logistics.decorator import chLogcsDr
from finance.decorator import chFncDr
from new31.func import frMtFee, rdrtBck
import time, datetime, math

# Create your views here.

def cart(request):
    u"""购物车"""
    cart = CartSess(request).show()

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

@login_required
def cnsgn(request):
    u"""收货人信息"""
    from logistics.forms import logcsFrm
    from finance.forms import fncFrm

    cnsgn = logcsFrm(request)
    fnc = fncFrm(request)

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


@postDrR('cart:cart')
@checkCartDr
@chLogcsDr
@chFncDr
def checkout(request):
    u"""购物车订单确认"""
    from logistics.views import LogcSess
    from finance.views import FncSess
    from order.views import OrdSess

    cart = CartSess(request).show()

    post = request.POST.dict()

    cInfo = LogcSess(request).setByDict(post).getObj() #将联系人信息存入session,并获得对应的对象
    fInfo = FncSess(request).setByDict(post).getObj() #将联系人信息存入session,并获得对应的对象
    OrdSess(request).frMt().setOrdtoNew().setUser()

    return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))


@postDrR('cart:cart')
@checkCartDr
@chLogcsDr
@chFncDr
@subDr
def submit(request):
    u"""购物车订单提交"""
    from order.views import OrdSub
    from message.models import Msg

    o = OrdSub(request).submit()
    if o.error:
        return o.showError()
    else:
        messages.success(request, u'您已成功提交订单!')
        messages.success(request, u'感谢您在本店购物！请记住您的订单号: %s' % o.sn)

        Msg.objects.pushToRole(-1, 7, 8, 9, 10, 12, 13, typ='success', msg='前台成功提交订单', data={'sn': o.sn} )

        if request.user.is_authenticated():
            return redirect('account:myOrd')
        else:
            return redirect('shop:shop')


@itemshow
def buy(request, sid):
    u"""加入购物车"""
    CartSess(request).pushBySid(int(sid))

    return redirect('cart:cart')


def delInCart(request, mark):
    u"""取出购物车"""
    CartSess(request).delete(int(mark))

    return rdrtBck(request)

@ajaxErrMsg('当前商品已下架')
def cNum(request, mark, num):
    u"""ajax-> 修改购物车中商品数量"""

    data =  f02f(CartSess(request).chngNum(int(mark), int(num)).total())

    return HttpResponse(Msg.objects.dumps(typ='success', data=data, msg='修改成功'))


from new31.cls import BsSess
class CartSess(BsSess):
    """
        购物车相关

        request.session['items']

        用于存储购物车中商品信息
        其数据格式为:
        [
            { 'mark':1, 'itemID':1, 'specID':1, 'num':1 },
            { 'mark':2, 'itemID':2, 'specID':2, 'num':2 },
            .........
        ]

        此类包含有对购物车操作的各类方法(必须实例化方可使用)

        example:
            CartSess(request).clear(mark)


    """
    def __init__(self, request):

        self.s = 'c'

        super(CartSess, self).__init__(request)

    def getMark(self):

        t = time.gmtime()
        tCount = t.tm_hour * t.tm_min * t.tm_sec
        sExpiryDate = self.request.session.get_expiry_date()
        sCount = (sExpiryDate.hour * sExpiryDate.minute * sExpiryDate.second ) % 10

        return int('%d%05d%d' % (len(self.sess) + 1, tCount, sCount ))


    def pushBySid(self, sid):
        from item.models import Item, ItemFee, ItemSpec
        from discount.models import Dis

        i = {
                'mark': self.getMark(),
                'itemID': Item.objects.getBySid(id=sid).id,
                'specID': ItemSpec.objects.getBySid(sid).id,
                'disID': Dis.objects.getBySid(id=sid).id if self.request.user.is_authenticated() else Dis.objects.default().id,
                'num': 1,
        }

        self.sess[i['mark']] = i

        return self._set()


    def pushByIDs(self, IDs):
        from item.models import Item
        from discount.models import Dis


        for i in IDs:
            ii = {
                    'mark': self.getMark(),
                    'itemID': i,
                    'specID': Item.objects.getByID(i).itemspec_set.default().id,
                    'disID': Dis.objects.default().id,
                    'num': 1,
            }

            self.sess[ii['mark']] = ii

        return self._set()


    def delete(self, mark):

        self.sess.pop(mark)

        return self.set(self.sess)


    def chngNum(self, mark, num):

        self.sess[mark]['num'] = num

        return self._set()


    def show(self):
        sess = self.sess.copy()

        items = []
        total = 0

        for i in self.sess:
            try:
                ii = self.getItem(i)
                total += ii['total']
                items.append(ii)
            except Exception, e:
                # raise e
                del sess[i]
                messages.warning(self.request, u'部分商品已下架。')

        self.set(sess)

        return {'items': items, 'total': frMtFee(total)}


    def total(self):

        return self.show()['total']

    def chngItem(self):

        name =  self.request.GET.get('name')
        mark =  self.request.GET.get('mark')
        value =  self.request.GET.get('value', 0)

        items = self.sess

        items[int(mark[1:])][name] = int(value)

        return self.set(items)

    def getItem(self, mark):
        from item.models import Item
        from discount.models import Dis

        i = self.sess[mark]

        item = Item.objects.getByID(id=i['itemID'])
        spec = item.itemspec_set.getBySid(id=i['specID'])
        dis = Dis.objects.get(id=i['disID'])
        fee = frMtFee(spec.itemfee_set.nomal().fee)
        nfee = frMtFee(fee * dis.dis)

        return {
                'mark': i['mark'],
                'item': item,
                'spec': spec,
                'fee': fee,
                'nfee': nfee,
                'num': i['num'],
                'dis': dis,
                'total': frMtFee(nfee * int(i['num']))
            }


    def copy(self, sn):

        return self.clear()._copy(sn)


    def _copy(self, sn):
        from order.models import Ord
        from item.models import ItemSpec
        from discount.models import Dis

        for i in Ord.objects.get(sn=sn).pro_set.all():
            spec = ItemSpec.objects.get(item__name=i.name, spec__value=i.spec)

            mark = self.getMark()

            self.sess[mark] = {
                                'mark': mark,
                                'itemID': spec.item.id,
                                'specID': spec.id,
                                'disID': Dis.objects.get(dis=i.dis).id,
                                'num': i.num,
                    }

        return self._set()