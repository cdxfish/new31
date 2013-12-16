#coding:utf-8
u"""支付"""
from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def pays(request):
    u"""支付方式"""
    from models import Pay

    pay = Pay.objects.select_related().all()

    return render_to_response('paylist.htm', locals(), context_instance=RequestContext(request))

def editPay(request, id):
    u"""编辑支付方式表单"""
    from models import Pay
    from forms import payFrm

    pay = Pay.objects.get(id=id)
    pay.form = payFrm(pay)

    return render_to_response('editpay.htm', locals(), context_instance=RequestContext(request))
