#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings 
from django.db.models import Q, Min
from item.models import Item
import random, json, os

# Create your views here.

# APP For Shop UI
def shop(request):
    itemList = ItemPin(10).buildItemList().sort(sortFun).itemList

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))

# 排序方法
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
       self.itemQuery = Item.objects.select_related().filter(Q(sn__contains='3133') | Q(sn__contains='3155') | Q(sn__contains='3177'))  #初始化物品序列

    # 获取物品数组
    def buildItemList(self):      
        for i in range(0, self.rowSize):

            lineItem = self.buildLineItem()

            self.itemList.append(lineItem)

        return self

    # 物品行排序方案,需传入一个函数对象
    def sort(self,function):
        self.itemList = function(self.itemList)

        return self

    # 从物品序列中随机获取一个物品,并以字典方式返回数据
    def randomItem(self):
        randomItem = random.choice(self.itemQuery)

        while not os.path.isfile('%simages\\%ss.jpg' % (settings.MEDIA_ROOT, randomItem.sn)):
            randomItem = random.choice(self.itemQuery)

        item = {
            'class': self.baseClass,    
            'img': '/m/%ss.jpg' % randomItem.sn,
            'name': randomItem.itemName,
            'sn': randomItem.sn,
            'like': randomItem.like,
            'click': randomItem.click,
            # 'amount': '%.2f' % randomItem.itemattr_set.all()[0].itemfee_set.get().amount,
        }
       
        # return item
        return self.varItemInfo(item)

    # 初始化物品行
    def buildLineItem(self):
        lineItem = []
        [lineItem.append(self.randomItem()) for i in range(0,self.lineSize)]

        if os.path.isfile('%simages\\%sb.jpg' % (settings.MEDIA_ROOT, lineItem[0]['sn'])):

            lineItem[0]['class'] = self.orthClass
            lineItem[0]['img'] = '/m/%sb.jpg' % lineItem[0]['sn']

        else:
            lineItem.append(self.randomItem())

        return lineItem

    # 获取物品信息
    def varItemInfo(self, item):
        item['amount'] = '%.2f' % Item.objects.select_related().get(sn='3133001').itemattr_set.all()[0].itemfee_set.get().amount

        return item