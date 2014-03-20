# coding: UTF-8
u"""积分"""
from django.shortcuts import render_to_response
from django.template import RequestContext

class Main(object):
    u"""积分"""

    def submit(self):
        u"""订单提交"""
        from django.contrib import messages

        try:
            oPt = self.ord.pro_set.all().total()
            pt = self.ord.user.pts.pt
            self.ord.user.pts.set(-oPt)
        except Exception, e:
            messages.success(self.request, u'会员帐号不存在或积分不足，无法支付。')
            raise e
        else:
            messages.success(self.request, u'用户积分已扣除')

            note = u'订单流程: %d | 积分 %d > %d' % ( self.ord.sn, pt, self.ord.user.pts.pt )
            self.ord.user.userlog.update(self.ord.user, self.request.user, note)
            # self.ord.fnc.cPay()

        return self

    def paid(self):
        pass

    def reimburse(self):
        u"""订单退款"""
        self.ord.user.pts.set(self.ord.pro_set.all().total())

        return self