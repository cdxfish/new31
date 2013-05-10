#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.db.models import Q
from item.models import *
from tag.models import *
import random


# Create your views here.

def randomTagShow(request):

    try:
        itemImgs = TagsObj().getItemByRandomTag()
    except:
        pass

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))
    
def tagShow(request, tag = ''):

    try:
        itemImgs = TagsObj().getItemByTag(tag)
    except:
        pass



    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))


def tagAdmin(request):

    tagList = Tag.objects.select_related().all().order_by('id')

    return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))


class GetItemByTag:
    """根据匹配到的tagTitle"""
    def __init__(self):
       self.item = ''
       self.itemQuery = Item.objects.getItemByAll()#初始化物品序列
       self.tagQuery = Tag.objects.select_related().all()  #初始化物品序列

    def getItem(self, tagTitle = ''):
        try:
            self.item = self.itemQuery.get(name=tagTitle)

        except Item.DoesNotExist:
            try:
                self.item = self.tagQuery.get(tag=tagTitle).item_set.order_by('?').all()[0]
            except:
                self.item = self.randomItem()
        else:
            self.item = self.itemQuery.get(name=tagTitle)

        # 检查当前item 是否存在图片. 避免进入死循环,只对上架商品进行一次遍历.
        try:
            if not self.item.itemimg_set.all():
                for i in self.itemQuery:
                    if self.item.itemimg_set.all():
                        break
                    else:
                        self.item = self.randomItem()

        except:
            pass

        return self

    def getOtherItem(self):
            pass


    def randomItem(self):
        try:
            return random.choice(self.itemQuery)
        except:
            pass

class TagsObj:
    """标签页相关"""
    tagsClass = {'tagsClass':['DD9797','BA5252','D97D0F','E3BA9B','71BFCD','95BADD','A7CF50',]}


    def getItemByTag(self, tag):
        items = Item.objects.getShowItemByTag(tag)

        itemImgs = []

        for i in items:
            for ii in i.itemimg_set.getImgByAll():

                itemImgs.append(ii)

        random.shuffle(itemImgs)

        return itemImgs




# 标签class用于前端html绑定
def tagsClass(request):

    return TagsObj.tagsClass