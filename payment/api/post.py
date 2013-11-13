#coding:utf-8
u"""货到刷卡"""
from __init__ import APIs

class main(APIs):
    """docstring for main"""
    def __init__(self, ord, *args, **kwarg):
        super(main, self).__init__(ord, *args, **kwarg)


    def sub(self):
        from message.models import Msg
        print Msg.objects.all()
        print 'post' * 20
        
        return self

    def pay(self):
        
        return self

    def re(self):
        
        return self