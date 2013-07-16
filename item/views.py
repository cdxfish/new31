#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from item.models import Item
from django.contrib.auth.models import User
import json

# Create your views here.

def item(request):

    return render_to_response('item.htm', locals(), context_instance=RequestContext(request))

def itemAdmin(request):
    itemList = ItemList().itemGetInfo().itemList

    # return HttpResponse(json.dumps(itemList))
    return render_to_response('itemadmin.htm', locals(), context_instance=RequestContext(request))    


def itemAdd(request):
    itemList = ItemList().itemGetInfo().itemList

    # return HttpResponse(json.dumps(itemList))
    return render_to_response('itemadd.htm', locals(), context_instance=RequestContext(request))    


class ItemList:
    """商品类 for Item"""
    def __init__(self):
        self.itemList = []
        self.itemQuery = Item.objects.select_related().all()  #初始化物品序列

    def itemGetInfo(self):
        for i in self.itemQuery:
            self.itemList.append( {
                'id': i.id,
                'itemName': i.itemName,
                'sn': i.sn,
                'onl': i.onl,
                'show': i.show,
                'like': i.like,
                'click': i.click,
            })

        return self