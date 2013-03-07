#coding:utf-8
from django.contrib import auth
from django.http import HttpResponse
from shop.views import *
import json

# Create your views here.

def ajaxLineItem(request):
    itemList = ItemPin(8).buildItemList().sort(sortFun).itemList

    return HttpResponse(json.dumps(itemList))