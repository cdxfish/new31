#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from item.models import Item
import random, json
from account.views import UserInfo

# Create your views here.

def shop(request):

    # item = Item.objects.all()

    return render_to_response('shop.htm', locals(), context_instance=RequestContext(request))
    # return HttpResponse(json.dumps(boxList.returnInfo()))

def randomBox():

    item = Item.objects.all()

    boxList = []
    for i in range(1, 10):
        # int(random.uniform(1,23))
        a = {'class':'b1','name':'xiangnong','img':'/m/3133001s.jpg'}
        b = {'class':'b1','name':'xiangnong','img':'/m/3133011s.jpg'}
        c = {'class':'b2','name':'xiangnong','img':'/m/3133001b.jpg'}
        box = [a, b, c]

        random.shuffle(box)

        boxList.append(box)

    return boxList