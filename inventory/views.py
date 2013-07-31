#coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.func import rdrtBck
from new31.decorator import rdrtBckDr
import datetime
# Create your views here.

def iUI(request):
    from models import InvNum

    pro = sort(InvNum.objects.getAll())

    return render_to_response('inventoryui.htm', locals(), context_instance=RequestContext(request))

def sort(pro):
    _pro = []

    for i in pro:
        __pro = {}
        for ii in i.invnum:
            sn = i.spec.item.sn
            __pro[sn] = {}
            __pro[sn]['name'] = i.spec.item.name

            if not hasattr(__pro[sn], 'invnum'):
                __pro[sn]['invnum'] = []

            __pro[sn]['invnum'].append(ii)
        _pro.append(__pro)


    return _pro


def iList(request):
    from item.models import Item

    items = Item.objects.getAll()

    return render_to_response('inventorylist.htm', locals(), context_instance=RequestContext(request))

@rdrtBckDr(u'该规格已下架')
def cOnl(request):
    from models import InvPro

    InvPro.objects.cOnl(int(request.GET.get('id')))

    return rdrtBck(request)

def default(request):
    from models import InvNum, InvPro
    InvNum.objects.default()

    return rdrtBck(request)

def minus(request):

    return rdrtBck(request)

def plus(request):

    return rdrtBck(request)