#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from new31.func import sort
import random


# Create your views here.

def randomShow(request):
    from models import Tag

    return tagShow(request, Tag.objects.random().tag)


def tagShow(request, tag):

    tagsCls = TagSrch.tagsCls

    items = sort(TagSrch(request).show(tag))[:8]

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))



class TagSrch(object):
    from decorator import noTagDr

    """
        标签页相关

    """

    tagsCls = ('DD9797','BA5252','D97D0F','E3BA9B','71BFCD','71BFCD','95BADD','95BADD','95BADD','A7CF50','A7CF50','A7CF50',)

    def __init__(self, request):
        self.items = []
        self.request = request


    def getTag(self, tag):
        from item.models import Item
        items = Item.objects.getShowByTag(tag)

        for i in items:
            Item.objects.click(i.id)
            
            for ii in i.itemimg_set.getBImgs():

                self.items.append(ii)

        return self

    @noTagDr
    def show(self, tag):

        return self.getTag(tag).items