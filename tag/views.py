#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib import messages
from message.decorator import ajaxErrMsg
from message.models import Msg
from new31.func import sort, f02f
import random


# Create your views here.

def randomShow(request):
    u"""随机标签"""
    from models import Tag

    return tagShow(request, Tag.objects.random().tag)


def tagShow(request, tag):
    u"""标签"""

    tagsCls = TagSrch.tagsCls

    # items = sort(TagSrch(request).show(tag))
    items = TagSrch(request).show(tag)

    return render_to_response('tag.htm', locals(), context_instance=RequestContext(request))

@ajaxErrMsg('无法修改数据')
def itemLike(request, id):
    u"""标签-> 商品喜欢"""
    from item.models import Item

    i = Item.objects.like(id=id)

    return HttpResponse(Msg.objects.dumps(data={'id': i.id, 'like': i.like}))

@ajaxErrMsg('当前商品已下架')
def getSpec(request, id):
    u"""标签-> 获取商品规格"""

    from item.models import ItemFee
    data = []
    for i in ItemFee.objects.getByItemId(id=id).filter(spec__item__show=True, spec__show=True).filter(typ=0):
        data.append({
            'id':i.spec.id ,
            'spec':i.spec.spec.value , 
            'fee': f02f(i.fee), 
            'nfee': f02f(i.nfee()), 
            })

        return HttpResponse(Msg.objects.dumps(data=data))

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