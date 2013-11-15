#coding:utf-8
u"""货到刷卡"""

class Main(object):
    u"""
        货到刷卡

    """
    urls = ()
    def sub(self):
        from message.models import Msg
        print Msg.objects.all()
        print 'post' * 20
        print self.ord

        return self

    def pay(self):
        
        return self

    def re(self):
        
        return self