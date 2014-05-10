# coding: UTF-8
u"""试吃"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def apply(request):
    u"""试吃"""
    from models import Apply

    applys = Apply.objects.all()

    return render_to_response('apply.htm', locals(), context_instance=RequestContext(request))


# @login_required
def tasting(request):
    u"""试吃申请"""
    from forms import ApplyFrm

    frm = ApplyFrm()

    return render_to_response('tasting.htm', locals(), context_instance=RequestContext(request))

def tastsave(request):
    u"""试吃提交"""
    from forms import ApplyFrm

    frm = ApplyFrm(request.POST)
    if frm.is_valid():
        new_user = frm.save()
        messages.error(request, u'申请提交成功')

    else:
        for i in frm:
            if i.errors:
                messages.error(request, u'%s - %s' % (i.label, i.errors))

    return redirect('tasting:tasting')