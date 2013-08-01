#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from item.decorator import itemonl
from new31.decorator import postDrR
from order.decorator import subDr
from new31.func import frMtFee, rdrtBck, rdrtIndex
import time, datetime, math
from decimal import Decimal

# Create your views here.

# 前台购物车界面
def cart(request):
    cart = CartSess(request).show()
    # from order.models import Ord
    # Ord.objects.all().delete()

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))


# 收货人信息界面
def cnsgn(request):
    from logistics.forms import logcsFrm
    from finance.forms import fncFrm

    cnsgn = logcsFrm(request)
    fnc = fncFrm(request)

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))



# 前台订单确认界面
@postDrR('/cart/')
def checkout(request):
    from logistics.forms import LogcsFrm
    from logistics.views import LogcSess
    from finance.views import FncSess
    from order.views import OrdSess

    post = request.POST.dict()

    cInfo = LogcSess(request).setByDict(post).getObj() #将联系人信息存入session,并获得对应的对象
    fInfo = FncSess(request).setByDict(post).getObj() #将联系人信息存入session,并获得对应的对象
    OrdSess(request).frMt().setSzero().setUser()


    form = LogcsFrm(post)

    if not form.is_valid():

        for i in form:
            if i.errors:

                messages.warning(request, '%s - %s' % ( i.label, u'这个字段是必填项。'))

        return rdrtBck(request)

    cart = CartSess(request).show()

    if not cart['items']:

        messages.warning(request, '购物车内无商品')

        return HttpResponseRedirect('/cart/')


    return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))

# 前台订单提交,并是用前台消息模板显示订单号等信息
@postDrR('/cart/')
# @subDr
def submit(request):
    from order.views import OrdSub

    o = OrdSub(request).submit()
    if o.error:
        return o.showError()
    else:
        messages.success(request, u'您已成功提交订单!')
        messages.success(request, u'感谢您在本店购物！请记住您的订单号: %s' % o.sn)

        if request.user.is_authenticated():
            return HttpResponseRedirect(request.nPath[u'我的订单'])
        else:
            return rdrtIndex()


# GET方式将物品放入购物车
# @itemonl
def buy(request):


    CartSess(request).pushBySid(request.GET.get('id'))
   
    # return rdrtBck(request)
    return HttpResponseRedirect('/cart/')

# GET方式将物品取出购物车
def delete(request):

    CartSess(request).delete(int(request.GET.get('id')))

    return rdrtBck(request)


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
                # 'disID': ItemFee.objects.getDisBySpecID(id=sid).id if self.request.user.is_authenticated() else Dis.objects.default().id,
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
                del sess[i]
                messages.warning(self.request, '部分商品已下架。')

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