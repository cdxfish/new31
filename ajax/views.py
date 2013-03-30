#coding:utf-8
from django.contrib import auth
from django.http import HttpResponse
from django.core.exceptions import *
from item.models import *
from shop.views import *
from cart.views import *
import json

# Create your views here.

def ajaxLineItem(request):
    itemList = ItemPin(8).buildItemList().sort(sortFun).itemList

    return HttpResponse(json.dumps(itemList))


def ajaxItemAttr(request, i, t = 1):
    data = {}
    try:
        itemAttr = ItemAttr.objects.getAttrByItemId(id=i)
        data['error'] = False
        data['message'] = ''
        data['data'] = []
        for v in itemAttr:
            try:
                data['data'].append({'id':v.id ,'attr':v.attrValue.attrValue ,'amount': '%s' % v.itemfee_set.get(itemType=t).amount,'t': t })
            except:
                pass
    except:
        data['error'] = True
        data['message'] = '当前商品已下架'

    return HttpResponse(json.dumps(data))


def ajaxCartItem(request, f, i, t = 1):
    try:
        f(request, i, t)

        return HttpResponse(AjaxRJson().error(False).data(request.session['itemCart']).jsonEn())
    except:

        return HttpResponse(AjaxRJson().error(True).message('当前商品已下架').data(request.session['itemCart']).jsonEn())


def ajaxCartItemNum(request, f, i, t):
    try:
        f(request, i, t)

        c = Cart(request)

        r ={'itemSubtotal': '%.2f' % c.cartItemSubtotal(i,t), 'subtotal': '%.2f' % c.countFee, 'i': i }

        return HttpResponse(AjaxRJson().error(False).data(r).jsonEn())
    except:

        return HttpResponse(AjaxRJson().error(True).message('当前商品已下架').data(request.session['itemCart']).jsonEn())


def cConsigneeByAjax(request):
    try:
        ShipConsignee().cCon(request)
        return HttpResponse(AjaxRJson().error(False).jsonEn())
    except:

        return HttpResponse(AjaxRJson().error(True).message('无法填写表单').jsonEn())


class AjaxRJson:
    """JSON 字典格式化"""
    def __init__(self):
        self.e = True
        self.m = ''
        self.d = {}

    def jsonEn(self):

        return json.dumps({'error':self.e, 'message':self.m, 'data':self.d })

    def error(self, e = True):
        self.e = e

        return self

    def message(self, m):
        self.m = m

        return self

    def data(self, d= {}):
        self.d = d

        return self