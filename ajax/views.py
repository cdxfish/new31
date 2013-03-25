#coding:utf-8
from django.contrib import auth
from django.http import HttpResponse
from shop.views import *
from item.models import *
import json

# Create your views here.

def ajaxLineItem(request):
    itemList = ItemPin(8).buildItemList().sort(sortFun).itemList

    return HttpResponse(json.dumps(itemList))



def ajaxItemAttr(request, i, t):
    data = {}
    try:
        item = Item.objects.get(id=i).itemattr_set.all()
        data['error'] = False
        data['message'] = ''
        data['item'] = []
        for v in item:
            data['item'].append( {'id':v.id ,'attr':v.attrValue.attrValue ,'amount': '%s' % v.itemfee_set.get(itemType=t).amount})
    except:
        data['error'] = True
        data['message'] = '当前商品不存在'


    return HttpResponse(json.dumps(data))

def ajaxItemBuy(request, i):
    if not request.session["buy"]:
        request.session["buy"] = {}

    data = {}
    try:
        item = ItemFee.objects.get(id=i)
        data['error'] = False
        data['message'] = ''
        data['item'] = {'id':item.id ,'attr':item.itemAttr.attrValue.attrValue ,'amount': '%s' % item.amount}
        if not i in request.session["buy"]:
            request.session["buy"].update({ i:1 })

        data['buy'] = request.session['buy']
    except:
        data['error'] = True
        data['message'] = '当前商品不存在'

    # request.session['buy'].clear()
    
    return HttpResponse(json.dumps(data))