#coding:utf-8
u"""积分"""
from django.shortcuts import render_to_response
from django.template import RequestContext

class Main(object):
    u"""
        积分

    """

    def sub(self):
        u"""订单提交"""
        from django.contrib import messages

        uPt = self.ord.user.pts
        oPt = self.ord.pro_set.all().pts()
        
        try:
            uPt.objects.set(oPt)
        except Exception, e:
            messages.success(self.request, u'积分不足，无法支付。')
            raise e
        else:
            messages.success(self.request, u'用户积分已扣除')

        return self

    def htm(request):
        u"""订单提交"""

        return render_to_response('office.htm', locals(), context_instance=RequestContext(request))

    urls = (
        (r'sub', htm),
        )
