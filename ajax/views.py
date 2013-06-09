#coding:utf-8
from django.contrib import auth
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import *
from item.models import *
from shop.views import *
from cart.views import *
from consignee.views import *
from order.views import *
import json

# Create your views here.

@tryMsg('无更多商品')
def getLineItemMore(request):
    itemList = ItemPin(8).buildItemList().sort(sortFun).itemList

    return AjaxRJson().jsonEn(itemList)


@tryMsg('当前商品已下架')
def getItemSpec(request, kwargs):

    itemSpec = ItemSpec.objects.getSpecByItemId(id=kwargs['specID'])

    data = [ {'id':i.id ,'spec':i.spec.value ,'amount': '%.2f' % i.itemfee_set.getFeeByNomal().amount, } for i in itemSpec ]

    return AjaxRJson().jsonEn(data)


@tryMsg('当前商品已下架')
def ajaxChangNum(request, kwargs):

    data =  '%.2f' % Cart(request).changeNumBySpec(mark=kwargs['mark'], num=kwargs['num']).countFee()

    return AjaxRJson().jsonEn(data)


def getItemByKeyword(request):

    @tryMsg('未找到商品')
    def _getItemByKeyword(request, kwargs):

        r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.getItemLikeNameOrSn( kwargs['k'] )]

        return AjaxRJson().jsonEn(r)

    return _getItemByKeyword(request=request, k=request.GET.get('k', ''))


# ajax动态写入收货人信息
@tryMsg('无法填写表单')
def cConsigneeByAjax(request, kwargs):
    ShipConsignee(request).setSeesion()

    return AjaxRJson().jsonEn()

# ajax动态写入收货人信息
@tryMsg('无法填写表单')
def coTypeByAjax(request, kwargs):
    o = OrderSubmit(request)
    o.oType = request.GET.get('oType')
    o.setSeesion()

    return AjaxRJson().jsonEn()


# ajax动态修改购物车内商品
@tryMsg('无法修改表单数据')
def cItemByAjax(request, kwargs):
    mark = int(request.GET.get('mark')[1:])
    cc = Cart(request).changeItem()

    i = cc.getItemTotalByMark(mark)

    data = {}
    data['mark'] = mark
    data['am'] = '%.2f' % i['amount']
    data['st'] = '%.2f' % i['total']
    data['total'] = '%.2f' % cc.countFee()

    return AjaxRJson().jsonEn(data)



# JSON数据格式化类
class AjaxRJson:
    """
        统一全局JSON 字典格式化

        {
            error: False,
            msg: 'success',
            data: {},
        }

    """
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