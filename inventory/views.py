#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.func import rdrtBck
from new31.decorator import rdrtBckDr
# Create your views here.

def iUI(request):

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))

def iList(request):
    from item.models import Item

    items = Item.objects.getAll()

    return render_to_response('inventorylist.htm', locals(), context_instance=RequestContext(request))

@rdrtBckDr(u'该规格已下架')
def cOnl(request):
    from models import InvPro

    InvPro.objects.cOnl(int(request.GET.get('id')))

    return rdrtBck(request)