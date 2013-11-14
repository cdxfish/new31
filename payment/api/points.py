#coding:utf-8
u"""积分"""

class Main(object):
    u"""
        积分

    """

    def sub(self):
        from django.contrib import messages

        uPt = self.ord.user.pts
        oPt = self.ord.pro_set.all().pts()
        
        if uPt.pt < oPt:
            messages.success(self.request, u'积分不足，无法支付。')

            raise
        else:

            pt.pt -=  1000
            pt.save()
            messages.success(self.request, u'用户积分已扣除')

        return self
