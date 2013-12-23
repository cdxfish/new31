#coding:utf-8
u"""支付"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
from new31.func import rdrtBck
from decorator import frmDr
# Create your views here.

def pays(request):
    u"""支付方式"""
    from models import Pay

    pay = Pay.objects.select_related().all()

    return render_to_response('paylist.htm', locals(), context_instance=RequestContext(request))

def editPay(request, id):
    u"""支付方式编辑表单"""
    from models import Pay
    from forms import payFrm

    pay = Pay.objects.get(id=id)
    pay.form = payFrm(pay)

    return render_to_response('editpay.htm', locals(), context_instance=RequestContext(request))

# @frmDr
def subEdit(request):
    u"""支付方式编辑提交"""
    from models import Pay
    from forms import PayFrm
    import json

    pay = Pay.objects.get(id=request.POST.get('id'))
    post = request.POST.dict()
    del post['id']
    del post['csrfmiddlewaretoken']

    pay.config = json.dumps(post)
    pay.save()

    messages.success(request, u'保存成功')

    return rdrtBck(request)