#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings 
from django.db.models import Q, Min
from item.models import Item
import random, json, os

# Create your views here.

def shop(request):
    # itemList = ItemPin(10).buildItemList().sort(sortFun).itemList

    itemQuery = Item.objects.select_related().get(id=1)
    itemQueryss = []
    for i in itemQuery.itemattr_set.all():
        a = i.itemfee_set.all()
        for b in a:
            itemQueryss.append(b)


    # return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))
    return HttpResponse(itemQueryss[1].amount)

def sortFun(itemList):
    [random.shuffle(i) for i in itemList]
    return itemList

class ItemPin:
    """瀑布流物品排序类"""
    def __init__(self, rowSize=8, lineSize=3, orthClass='b2', baseClass='b1'):
       self.rowSize = rowSize
       self.lineSize = lineSize
       self.orthClass = orthClass
       self.baseClass = baseClass

       self.itemList = []
       self.itemQuery = Item.objects.filter(Q(sn__contains='3133') | Q(sn__contains='3155') | Q(sn__contains='3177')) 

    def buildItemList(self):      
        for i in range(0, self.rowSize):

            lineItem = self.buildLineItem()

            self.itemList.append(lineItem)

        return self

    def sort(self,function):
        self.itemList = function(self.itemList)
        # [random.shuffle(i) for i in self.itemList]

        return self

    def randomItem(self):
        randomItem = random.choice(self.itemQuery)

        while not os.path.isfile('%simages\\%ss.jpg' % (settings.MEDIA_ROOT, randomItem.itemAttr.itemName.sn)):
            randomItem = random.choice(self.itemQuery)

        item = {
            'class': self.baseClass,    
            'img': '/m/%ss.jpg' % randomItem.itemAttr.itemName.sn,
            'name': randomItem.itemAttr.itemName,
            'sn': randomItem.itemAttr.itemName.sn,
            'price':randomItem.amount,
        }
       
        return item

    def buildLineItem(self):
        lineItem = []
        [lineItem.append(self.randomItem()) for i in range(0,self.lineSize)]

        if os.path.isfile('%simages\\%sb.jpg' % (settings.MEDIA_ROOT, lineItem[0]['sn'])):

            lineItem[0]['class'] = self.orthClass
            lineItem[0]['img'] = '/m/%sb.jpg' % lineItem[0]['sn']

        else:
            lineItem.append(self.randomItem())

        return lineItem