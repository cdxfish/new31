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
    from item.models import Item

    items = Item.objects.getShowByTag(tag)


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
    for i in ItemFee.objects.getByItemId(id=id).filter(typ=0, spec__item__show=True, spec__show=True):
        data.append({
            'id':i.spec.id ,
            'spec':i.spec.spec.value ,
            'fee': f02f(i.fee),
            'nfee': f02f(i.nfee()),
            })

    return HttpResponse(Msg.objects.dumps(data=data))