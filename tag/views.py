#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q, Min
from item.models import Item
from tag.models import Tag
import random


# Create your views here.

def tag(request, tagTitle = ''):
    # item = Tag.objects.select_related().all().get(tag=tagTitle).item_set.all()[0]


    item = GetItemByTag().getItem(tagTitle=tagTitle).item

    # d = dir(item.itemdesc_set.random().desc)




    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

def tagAdmin(request):


    return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))





class GetItemByTag:
    """根据匹配到的tagTitle"""
    def __init__(self):
       self.item = ''
       self.itemQuery = Item.objects.select_related().filter( \
                            Q(sn__contains='3133') | \
                            Q(sn__contains='3155') | \
                            Q(sn__contains='3177') | \
                            Q(onLine=True) | \
                            Q(show=True))  #初始化物品序列
       self.tagQuery = Tag.objects.select_related().all()  #初始化物品序列

    def getItem(self, tagTitle = ''):
        try:
            self.item = self.itemQuery.get(itemName=tagTitle)
            # self.item.update()
        except Item.DoesNotExist:
            self.item = self.tagQuery.get(tag=tagTitle).item_set.order_by('?').all()[0]
        except:
            self.item = self.randomItem()


        # 检查当前item 是否存在图片. 未避免进入死循环,只对上架商品进行一次遍历.

        if not self.item.itemimg_set.all():
            for i in self.itemQuery:
                if self.item.itemimg_set.all():
                    break
                else:
                    self.item = self.randomItem()

        return self

    def getOtherItem(self):
            pass


    def randomItem(self):
        return random.choice(self.itemQuery)