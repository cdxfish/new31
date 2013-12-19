#coding:utf-8
u"""积分"""
from django.shortcuts import render_to_response
from django.template import RequestContext

class Main(object):
    u"""积分"""

    def sub(self):
        u"""订单提交"""
        from django.contrib import messages

        oPt = self.ord.pro_set.all().total()

        try:
            self.ord.user.pts.set(-oPt)
        except Exception, e:
            messages.success(self.request, u'积分不足，无法支付。')
            raise e
        else:
            messages.success(self.request, u'用户积分已扣除')

        return self

    def re(self):
         u"""订单退款"""
        from django.contrib import messages

        oPt = self.ord.pro_set.all().total()
        try:
            self.ord.user.pts.set(oPt)
        except Exception, e:
            messages.success(self.request, u'积分无法退还至帐户。')
            raise e
        else:
            messages.success(self.request, u'积分已退还至帐户。')

        return self