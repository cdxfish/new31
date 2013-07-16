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

# 首页瀑布流获取更多商品
# @tryMsg('无更多商品')
def getItemPin(request):

    return AjaxRJson().dumps(ItemPin(8).getItems(sort))


# 前台弹出层中获取商品规格
@tryMsg('当前商品已下架')
def getItemSpec(request, kwargs):

    itemSpec = ItemSpec.objects.getSpecByItemId(id=kwargs['specID'])

    data = [ {'id':i.id ,'spec':i.spec.value ,'fee': '%.2f' % i.itemfee_set.getFeeByNomal().fee, } for i in itemSpec ]

    return AjaxRJson().dumps(data)


# 前台购物车界面修改购物车中商品数量
@tryMsg('当前商品已下架')
def ajaxChangNum(request, kwargs):

    data =  '%.2f' % Cart(request).changeNumBySpec(mark=kwargs['mark'], num=kwargs['num']).countFee()

    return AjaxRJson().dumps(data)


# 商品查询，后台新订单及订单编辑用
def getItemByKeyword(request):

    @tryMsg('未找到商品')
    def _getItemByKeyword(request, kwargs):

        r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.getItemLikeNameOrSn( kwargs['k'] )]

        return AjaxRJson().dumps(r)

    return _getItemByKeyword(request=request, k=request.GET.get('k', ''))


# ajax动态写入收货人信息
@tryMsg('无法填写表单')
def cConsigneeByAjax(request, kwargs):
    ShipConsignee(request).setSeesion()

    return AjaxRJson().dumps()

# ajax动态写入收货人信息
@tryMsg('无法填写表单')
def coTypeByAjax(request, kwargs):

    o = Order(request)

    o.o['typ'] = request.GET.get('oType')

    return AjaxRJson().dumps()


# ajax动态修改购物车内商品
@tryMsg('无法修改表单数据')
def cItemByAjax(request, kwargs):
    mark = int(request.GET.get('mark')[1:])
    cc = Cart(request).changeItem()

    i = cc.getItemTotalByMark(mark)

    data = {}
    data['mark'] = mark
    data['am'] = '%.2f' % i['fee']
    data['st'] = '%.2f' % i['total']
    data['total'] = '%.2f' % cc.countFee()

    return AjaxRJson().dumps(data)



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

    def dumps(self, data=''):
        if data:
            self.data = data

        return HttpResponse(json.dumps({'err':self.error, 'msg':self.msg, 'data':self.data }))

    def message(self, msg = ''):
        
        self.msg = msg
        self.error = True

        return self