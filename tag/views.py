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

    a = dir(Tag())

    itemImgs = TagsObj().getItemByRandomTag()

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))


def tagShow(request, tag = ''):

    itemImgs = TagsObj().getItemByTag(tag)

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))


def tagAdmin(request):

    tagList = Tag.objects.select_related().all().order_by('id')

    return render_to_response('tagadmin.htm', locals(), context_instance=RequestContext(request))


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

    def getItemByRandomTag(self):
        tag = Tag.objects.getRandom()

        itemImgs = self.getItemByTag(tag.tag)


        if not itemImgs:
            # 未避免死循环只进行一遍遍历
            for i in Tag.objects.getTagByAll().order_by('?'):
                itemImgs += self.getItemByTag(i.tag)

        return itemImgs