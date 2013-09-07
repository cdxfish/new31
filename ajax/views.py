#coding:utf-8
u"""ajax"""
from django.http import HttpResponse
from decorator import ajaxMsg
from logistics.decorator import aLogcsDr
from new31.func import sort, f02f, frMtFee
from new31.cls import AjaxRJson
import json

# Create your views here.

@ajaxMsg('无更多商品')
def getItemPin(request):
    u"""首页-> 获取更多商品"""
    from shop.views import ItemPin

    return AjaxRJson().dumps(ItemPin(8).getItems(sort))

@ajaxMsg('无法修改数据')
def itemLike(request, id):
    u"""标签-> 商品喜欢"""
    from item.models import Item

    i = Item.objects.like(id=id)

    return AjaxRJson().dumps({'id': i.id, 'like': i.like})

@ajaxMsg('当前商品已下架')
def getSpec(request, id):
    u"""标签-> 获取商品规格"""

    from item.models import ItemFee
    data = []
    for i in ItemFee.objects.getByItemId(id=id).filter(spec__item__show=True, spec__show=True).filter(typ=0):
        data.append({
            'id':i.spec.id ,
            'spec':i.spec.spec.value , 
            'fee': f02f(i.fee), 
            'nfee': f02f(i.nfee()), 
            })

    return AjaxRJson().dumps(data)

@ajaxMsg('当前商品已下架')
def cNum(request):
    u"""购物车-> 修改购物车中商品数量"""
    from cart.views import CartSess
    mark = int(request.GET.get('mark'))
    num = int(request.GET.get('num'))

    data =  f02f(CartSess(request).chngNum(mark, num).total())

    return AjaxRJson().dumps(data)

@ajaxMsg('无法填写表单')
def cLogcs(request):
    u"""购物车-> 修改收货人信息"""
    from logistics.views import LogcSess

    for i,v in request.GET.dict().items():
        LogcSess(request).setByName(i, u'%s' % v)

    return AjaxRJson().dumps()

@ajaxMsg('无法修改表单数据')
def cItem(request):
    u"""购物车-> 修改购物车内商品"""
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

@ajaxMsg('无法修改表单数据')
@aLogcsDr
def cAdv(logcs, value):
    u"""物流-> 修改物流偏移量"""

    logcs.advance = value

@ajaxMsg('无法修改表单数据')
@aLogcsDr
def cDman(logcs, value):
    u"""物流-> 修改物流师傅"""
    if value:
        from django.contrib.auth.models import User

        user = User.objects.get(id=value)
        logcs.dman = user
    else:
        logcs.dman = None

@ajaxMsg('未找到商品')
def getItemByKeyword(request):
    u"""订单-> 商品查询"""
    from item.models import Item

    r = [ { 'name':i.name, 'sn': i.sn, 'id': i.id, } for i in Item.objects.likeNameOrSn(request.GET.get('k', ''))]

    return AjaxRJson().dumps(r)

@ajaxMsg('无此会员')
def getUser(request):
    u"""订单-> 查询会员"""
    from account.models import BsInfo

    u = BsInfo.objects.get(user__username=request.GET.get('u'))

    return AjaxRJson().dumps({
            u'用户名': u.user.username,
            u'姓名': '%s %s' % (u.user.last_name, u.user.first_name),
            u'生日': '%s %s' % (u.get_mon_display(), u.get_day_display()),
            u'性别': u.get_sex_display(),
            u'类型': u.get_typ_display(),
            u'邮箱': u.user.email,
            u'积分': u.user.pts.pt,
            u'注册时间': '%s' % u.user.date_joined,
        })

@ajaxMsg('无法填写表单')
def cFnc(request):
    u"""订单-> 修改财务信息"""
    from finance.views import FncSess
    for i,v in request.GET.dict().items():
        FncSess(request).setByName(i, v)

    return AjaxRJson().dumps()

@ajaxMsg('无法填写表单')
def cOrd(request):
    u"""订单-> 修改订单信息"""
    from order.views import OrdSess
    for i,v in request.GET.dict().items():
        OrdSess(request).setByName(i, v)

    return AjaxRJson().dumps()