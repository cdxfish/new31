#coding:utf-8
from django.http import HttpResponse
from decorator import ajaxMsg
from logistics.decorator import aLogcsDr
from new31.func import sort, f02f
import json

# Create your views here.

# 首页瀑布流获取更多商品
@ajaxMsg('无更多商品')
def getItemPin(request):
    from shop.views import ItemPin

    return AjaxRJson().dumps(ItemPin(8).getItems(sort))


# 前台弹出层中获取商品规格
@ajaxMsg('当前商品已下架')
def getSpec(request):
    from item.models import ItemSpec

    return AjaxRJson().dumps([ {'id':i.id ,'spec':i.spec.value ,'fee': f02f(i.itemfee_set.nomal().fee), } for i in ItemSpec.objects.getByitemID(id=request.GET.get('id')) ])


# 前台购物车界面修改购物车中商品数量
@ajaxMsg('当前商品已下架')
def cNum(request):
    from cart.views import CartSess
    mark = int(request.GET.get('mark'))
    num = int(request.GET.get('num'))

    data =  f02f(CartSess(request).chngNum(mark, num).total())

    return AjaxRJson().dumps(data)


# 商品查询，后台新订单及订单编辑用
@ajaxMsg('未找到商品')
def getItemByKeyword(request):
    from item.models import Item

    r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.likeNameOrSn(request.GET.get('k', ''))]

    return AjaxRJson().dumps(r)



# ajax动态写入收货人信息
@ajaxMsg('无法填写表单')
def cLogcs(request):
    from logistics.views import LogcSess

    for i,v in request.GET.dict().items():
        LogcSess(request).setByName(i, v)

    return AjaxRJson().dumps()

# ajax动态写入订单信息
@ajaxMsg('无法填写表单')
def cOrd(request):
    from order.views import OrdSess
    for i,v in request.GET.dict().items():
        OrdSess(request).setByName(i, v)

    return AjaxRJson().dumps()

# ajax动态写入财务信息
@ajaxMsg('无法填写表单')
def cFnc(request):
    from finance.views import FncSess
    for i,v in request.GET.dict().items():
        FncSess(request).setByName(i, v)

    return AjaxRJson().dumps()


# ajax动态修改购物车内商品
@ajaxMsg('无法修改表单数据')
def cItem(request):
    from cart.views import CartSess
    mark = int(request.GET.get('mark')[1:])
    cc = CartSess(request).chngItem()

    i = cc.getItem(mark)



    return AjaxRJson().dumps({
        'mark': mark,
        'fee': f02f(i['fee']),
        'nfee': f02f(i['nfee']),
        'st': f02f(i['total']),
        'total': f02f(cc.total()),
    })

# ajax动态修改物流偏移量
@ajaxMsg('无法修改表单数据')
@aLogcsDr
def cAdv(logcs, value):

    logcs.advance = value




# ajax动态修改物流师傅
@ajaxMsg('无法修改表单数据')
@aLogcsDr
def cDman(logcs, value):
    if value:
        from django.contrib.auth.models import User

        user = User.objects.get(id=value)
        logcs.dman = user
    else:
        logcs.dman = None


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