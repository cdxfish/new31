#coding:utf-8
u"""消息"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from new31.cls import AjaxRJson
from decorator import readDr
# Create your views here.

def get(request):
    u"""消息推送"""
    from models import Msg

    return AjaxRJson().dumps([ {'id':i.id, 'data':i.data(), 'typ': i.get_typ_display(), 'time': '%s' % i.time.strftime('%Y-%m-%d %H:%M:%S')} for i in Msg.objects.get(request.user) ])

@readDr
def read(request):
    u"""消息已读"""
    from models import Msg
    ids = request.GET.getlist('id[]')

    Msg.objects.read(*ids)

    return AjaxRJson().dumps(ids)
