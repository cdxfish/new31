#coding:utf-8
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import *
from item.models import *
from shop.views import *
from cart.views import *
from consignee.views import *
import json

# Create your views here.

def getLineItemMore(request):
    itemList = ItemPin(8).buildItemList().sort(sortFun).itemList

    return AjaxRJson().jsonEn(itemList)


def getItemSpec(request, i, t = 1):
    try:
        itemSpec = ItemSpec.objects.getSpecByItemId(id=i)

        data = {{'id':v.id ,'spec':v.spec.value ,'amount': '%s' % v.itemfee_set.get(itemType=t).amount,'t': t } for v in itemSpec}

        return AjaxRJson().jsonEn(data)

    except:
        return AjaxRJson().message('当前商品已下架').jsonEn()



def ajaxCartItemNum(request, f, i, t):
    try:
        f(request, i, t)

        c = Cart(request)

        r ={'itemSubtotal': '%.2f' % c.cartItemSubtotal(i,t), 'subtotal': '%.2f' % c.countFee, 'i': i }

        return AjaxRJson().jsonEn(r)
    except:

        return AjaxRJson().message('当前商品已下架').jsonEn(request.session['itemCart'])

def itemByKeyword(request):
    k = request.GET.get('k') if request.GET.get('k') else ''

    if settings.DEBUG:

        return getItemByKeyword(k)

    else:

        try:

            return getItemByKeyword(k)
        except:

            return AjaxRJson().error(True).message('未找到商品').data(request.session['itemCart']).jsonEn()


def getItemByKeyword(k):

    r = { i.id: {'name':i.name, 'sn': i.sn} for i in Item.objects.getItemLikeNameOrSn(k)}

    return AjaxRJson().jsonEn(r)



# ajax动态写入收货人信息
def cConsigneeByAjax(request):
    try:

        ShipConsignee(request).saveConsignee()

        return AjaxRJson().jsonEn()
    except:

        return AjaxRJson().message('无法填写表单').jsonEn()



class AjaxRJson:
    """JSON 字典格式化"""
    def __init__(self):
        self.error = False
        self.msg = 'success'
        self.data = {}

    def jsonEn(self, data=''):
        if data:
            self.data = data

        return HttpResponse(json.dumps({'error':self.error, 'message':self.msg, 'data':self.data }))

    def message(self, msg = ''):
        
        self.msg = msg
        self.error = True

        return self