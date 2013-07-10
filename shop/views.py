#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings 
from django.db.models import Q, Min
from item.models import *
from tag.models import *
import random, json, os
from django.contrib import messages

# Create your views here.

# APP For Shop UI
def shop(request):

    items = ItemPin(10).getItems()

    tags = Tag.objects.all()[:8]

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))

# 排序方法
def sortFun(itemList):
    [random.shuffle(i) for i in itemList]
    return itemList

class ItemPin(object):
    """
        瀑布流物品排序类
        用于首页物品展示用
        可看作矩阵

        实例化参数: 

        rSize(竖尺寸)
        lSize(横尺寸)

        使用方法: ItemPin(10).getItems()

        方便前台ajax调用, 返回值为列表, 格式为.

        [
            {
                'name': 'xxx', 
                'amount': '￥ %0.2f', 
                'like': 123, 
                'src': 'http://xxxxxx.jpg',
                'width': 123,
                'height': 123
             },
            .............
            ,
            .............
            ,
        ]

    """
    def __init__(self, rSize=8, lSize=(1,2)):
       self.rSize = rSize
       self.lSize = sum(lSize)

       self.itemQuery = ItemImg.objects.getSImgs()  #初始化物品序列
       self.matrix = []

    """
        矩阵竖坐标

        长度为rowSize


    """
    def buildRow(self, rSize):

        for x in xrange(0, rSize):

            self.builLine(self.lSize)

        return self


    """
        矩阵横坐标

        长度为lineSize

    """
    def builLine(self, lSize):
        lItems = []
        for x in xrange(0,lSize):
            i =  self.random()

            self.matrix.append({
                        'name': i.item.name, 
                        'amount': '￥ %0.2f' % i.item.itemspec_set.getDefaultSpec().itemfee_set.getFeeByNomal().amount, 
                        'like': i.item.like, 
                        'src': i.img.url,
                        'width': i.img.width,
                        'height': i.img.height
                    })

        return self

    def getItems(self):
 
        return self.buildRow(self.rSize).matrix

    def random(self):

        return random.choice(self.itemQuery)

    def sort(self):
        for x in self.matrix:
            pass

        return self