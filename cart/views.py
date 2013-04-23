#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.exceptions import *
from item.models import *
from account.models import *
from payment.models import *
from signtime.models import *
from area.models import *
from order.models import *
from message.views import *
import time, datetime

# Create your views here.

def cart(request):
    a = request.user
    b = dir(a)

    cart = Cart(request)

    return render_to_response('cart.htm', locals(), context_instance=RequestContext(request))

def hCart(request, f, i, t = 1):
    try:
        f(request, i, t)

        return HttpResponseRedirect("/cart/")
    except:
        return Message(request, request.META.get('HTTP_REFERER',"/")).autoRedirect(3).title('错误').message('当前商品已下架!').shopMsg()


def consignee(request):

    pay = Pay.objects.filter(onLine=True)
    signtime = SignTime.objects.filter(onLine=True)

    area = Area.objects.filter(onLine=True,sub=None)

    toDay = time.gmtime()
    cDate = time.strptime(request.session['c']['date'], '%Y-%m-%d')

    if cDate < toDay:
        request.session['c']['date'] = '%s' % datetime.date.today()

    return render_to_response('consignee.htm', locals(), context_instance=RequestContext(request))


def checkout(request):
    # 配置当session
    try:
        ShipConsignee().cConFormPOST(request)

    except:
        return Message(request, request.META.get('HTTP_REFERER',"/")).autoRedirect(3).title('错误').message('请重新填写收货人信息!').shopMsg()


    cart = Cart(request)

    pay = Pay.objects.get(onLine=True, id=request.session['c']['pay'])
    time = SignTime.objects.get(onLine=True, id=request.session['c']['time'])

    area = Area.objects.get(onLine=True, id=request.session['c']['area'])

    return render_to_response('checkout.htm', locals(), context_instance=RequestContext(request))


def buyToCart(request, i , t= 1):
    try:
        item = Item.objects.getItemByItemSpecId(id=i)

        itemCart = request.session["itemCart"]

        if not i in itemCart:
            itemCart.update({ '%s%s' % (t,i):1 })

        request.session['itemCart'] = itemCart

        return request
    except:
        raise  Item.DoesNotExist


def clearCartItem(request, i , t= 1):
    try:
        if not request.session.get('itemCart'):
            request.session["itemCart"] = {}

        itemCart = request.session["itemCart"]

        a = '%s%s' % (t,i)

        if a in itemCart:
            del itemCart[a]

        request.session['itemCart'] = itemCart

        return request
    except:
        raise Item.DoesNotExist

def changeCartItem(request, i , t):
    try:
        item = Item.objects.getItemByItemAttrId(id='%s' % i[1:])

        itemCart = request.session["itemCart"]

        if i in itemCart:
            itemCart[i] = int(t)

        request.session['itemCart'] = itemCart

        return request
    except:
        raise Item.DoesNotExist


def cConsigneeByCart(request):
    try:
        ShipConsignee().cConFormGET(request)

        return HttpResponseRedirect("/cart/consignee/")
    except:
        return Message(request, request.META.get('HTTP_REFERER',"/")).autoRedirect(3).title('错误').message('无法保存信息!').shopMsg()


class Cart:
    """docstring for Cart"""
    def __init__(self, request):
        self.itemBuy = []
        self.countFee = 0
        self.request = request
        if self.request.session.get('itemCart'):
            for v, i in self.request.session['itemCart'].items():
                try:
                    if len(v) < 2:
                        raise Item.DoesNotExist
                        
                    itemSpec = ItemSpec.objects.getSpecByItemSpecId(id='%s' % v[1:])
                    amount = itemSpec.itemfee_set.get(itemType=v[0]).amount
                    subtotal = amount * i
                    self.countFee += subtotal
                    self.itemBuy.append({ 'item': itemSpec, 'amount': amount, 'num': i,'subtotal': subtotal, 'v': v })
                except:
                    pass

    def cartItemSubtotal(self, i, t):
        itemCart = self.request.session["itemCart"]
        itemSubtotal = ItemSpec.objects.getSpecByItemSpecId(id='%s' % i[1:]).itemfee_set.get(itemType=i[0]).amount * int(t)

        return itemSubtotal

class ShipConsignee:
    """docstring for Consignee"""
    def __init__(self):
        pass      

    def cConFormGET(self, request):
        try:
            if request.GET:
                n = request.GET
            else:
                raise ValueError

            s = request.session['c']

            for v,i in n.items():
                # 用于下拉框默认值,使得过滤器辨别为false
                if i == '0':
                    s[v] = 0
                else:
                    s[v] = i

            request.session['c'] = s

            return self
        except:
            raise ValueError

    def cConFormPOST(self, request):
        try:
            if request.POST:
                n = request.POST
            else:
                raise ValueError

            s = request.session['c']

            for v,i in n.items():
                # 用于下拉框默认值,使得过滤器辨别为false
                if i == '0':
                    s[v] = 0
                else:
                    s[v] = i

            request.session['c'] = s

            return self
        except:
            raise ValueError