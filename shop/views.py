#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.conf import settings 
from django.db.models import Q
from item.models import Item
import random, json, os

# Create your views here.

def shop(request):

    itemList = ItemPin(10).sort()

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))
    # return HttpResponse(json.dumps(itemList.returnInfo()))


class ItemPin:
    """瀑布流物品排序类"""
    def __init__(self, rowSize=8, lineSize=3):
       self.rowSize = rowSize
       self.lineSize = lineSize

    def sort(self):      
        item = Item.objects.filter(Q(sn__contains='3133')|Q(sn__contains='3155')|Q(sn__contains='3177')) 
        # randomItem = int(random.uniform(1,item.count()))

        itemList = []
        for i in range(0, self.rowSize):
            aItem = item[int(random.uniform(1,item.count()))]
            bItem = item[int(random.uniform(1,item.count()))]
            cItem = item[int(random.uniform(1,item.count()))]

            while not os.path.isfile('%simages\\%ss.jpg' % (settings.MEDIA_ROOT, aItem.sn)):
                aItem = item[int(random.uniform(1,item.count()))]
            else:
                aItem.img = '/m/%ss.jpg' % aItem.sn

            while not os.path.isfile('%simages\\%ss.jpg' % (settings.MEDIA_ROOT, bItem.sn)):
                bItem = item[int(random.uniform(1,item.count()))]
            else:
                bItem.img = '/m/%ss.jpg' % bItem.sn

            while not os.path.isfile('%simages\\%sb.jpg' % (settings.MEDIA_ROOT, cItem.sn)):
                cItem = item[int(random.uniform(1,item.count()))]
            else:
                cItem.img = '/m/%sb.jpg' % cItem.sn

            a = {'class':'b1','name':aItem.name,'img':aItem.img}
            b = {'class':'b1','name':bItem.name,'img':bItem.img}
            c = {'class':'b2','name':cItem.name,'img':cItem.img}
            box = [a, b, c]

            random.shuffle(box)

            itemList.append(box)

        return itemList