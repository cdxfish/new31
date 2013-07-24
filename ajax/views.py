#coding:utf-8
from django.http import HttpResponse
from new31.decorator import errMsg
import json

# Create your views here.

# 首页瀑布流获取更多商品
@errMsg('无更多商品')
def getItemPin(request, kwargs):

    return AjaxRJson().dumps(ItemPin(8).getItems(sort))


# 前台弹出层中获取商品规格
@errMsg('当前商品已下架')
def getItemSpec(request, kwargs):
    from item.models import ItemSpec

    itemSpec = ItemSpec.objects.getSpecByItemId(id=kwargs['specID'])

    data = [ {'id':i.id ,'spec':i.spec.value ,'fee': '%.2f' % i.itemfee_set.getFeeByNomal().fee, } for i in itemSpec ]

    return AjaxRJson().dumps(data)


# 前台购物车界面修改购物车中商品数量
@errMsg('当前商品已下架')
def ajaxChangNum(request, kwargs):
    from cart.views import Cart

    data =  '%.2f' % Cart(request).changeNumBySpec(mark=kwargs['mark'], num=kwargs['num']).countFee()

    return AjaxRJson().dumps(data)


# 商品查询，后台新订单及订单编辑用
def getItemByKeyword(request):

    @errMsg('未找到商品')
    def _getItemByKeyword(request, kwargs):
        from item.models import Item

        r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.getItemLikeNameOrSn( kwargs['k'] )]

        return AjaxRJson().dumps(r)

    return _getItemByKeyword(request=request, k=request.GET.get('k', ''))


# ajax动态写入收货人信息
@errMsg('无法填写表单')
def cCnsgnByAjax(request, kwargs):
    from logistics.views import Cnsgn
    Cnsgn(request).setSeesion()

    return AjaxRJson().dumps()

# ajax动态写入收货人信息
@errMsg('无法填写表单')
def coTypeByAjax(request, kwargs):

    o = Ord(request)

    o.o['typ'] = int(request.GET.get('oType'))

    return AjaxRJson().dumps()


# ajax动态修改购物车内商品
@errMsg('无法修改表单数据')
def cItemByAjax(request, kwargs):
    from cart.views import Cart
    mark = int(request.GET.get('mark')[1:])
    cc = Cart(request).changeItem()

    i = cc.getItemTotalByMark(mark)

    data = {}
    data['mark'] = mark
    data['am'] = '%.2f' % i['fee']
    data['st'] = '%.2f' % i['total']
    data['total'] = '%.2f' % cc.countFee()

    return AjaxRJson().dumps(data)

# ajax动态修改物流偏移量
@errMsg('无法修改表单数据')
def cAdv(request, kwargs):
    from order.models import OrdLogcs

    sn = int(request.GET.get('sn')[1:])
    value = int(request.GET.get('value', 0))

    logcs = OrdLogcs.objects.get(ord=sn)

    if logcs.ord.ordship.status > 1:
        return AjaxRJson.message(u'无法修改表单数据').dumps()

    logcs.advance = value

    logcs.save()

    data = {}
    data['sn'] = sn
    data['value'] = value

    return AjaxRJson().dumps(data)

# ajax动态修改物流师傅
@errMsg('无法修改表单数据')
def cDman(request, kwargs):
    sn = int(request.GET.get('sn')[1:])
    value = int(request.GET.get('value', 0))

    from order.models import OrdLogcs
    logcs = OrdLogcs.objects.get(ord=sn)

    if logcs.ord.ordship.status > 1:
        return AjaxRJson.message(u'无法修改表单数据').dumps()

    if value:
        from django.contrib.auth.models import User
        user = User.objects.get(id=value)
        logcs.dman = user
    else:
        logcs.dman = None

    logcs.save()

    data = {}
    data['sn'] = sn
    data['value'] = value

    return AjaxRJson().dumps(data)


def cLogcs(request, func):
    sn = int(request.GET.get('sn')[1:])
    value = int(request.GET.get('value', 0))

    from order.models import OrdLogcs
    logcs = OrdLogcs.objects.get(ord=sn)

    if logcs.ord.ordship.status > 1:
        return AjaxRJson.message(u'无法修改表单数据').dumps()

    return func()



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