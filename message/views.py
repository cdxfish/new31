#coding:utf-8
u"""消息"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import dateformat
from django.http import HttpResponse
from models import Msg
from new31.cls import UTC
from decorator import readDr
# Create your views here.

def get(request):
    u"""消息推送"""
    from models import Msg

    return HttpResponse(Msg.objects.dumps(data=[
        dict({
                'id':i.id,
                'time': '%s' % i.time.astimezone(UTC(8)).strftime('%Y-%m-%d %H:%M:%S'),
            }, **i.data() )
            for i in Msg.objects.get(request.user)
        ])
    )

@readDr
def read(request):
    u"""消息已读"""
    from models import Msg
    ids = request.GET.getlist('id[]')

    Msg.objects.read(*ids)

    return HttpResponse(Msg.objects.dumps(data=ids))