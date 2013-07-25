#coding:utf-8


class BsSess(object):
    """
        session
        基本类
        APP中各session控制均继承于此

    """
    def __init__(self, request):
        self.request = request

        if not hasattr(self, 's'):
            self.s = 's'

        if not hasattr(self,'frmt'):
            self.frmt = {}

        self.sess = self.request.session.get(self.s)

    # 初始化seesion中用于存储订单的基本操作信息字典
    def frMt(self):
        if not self.sess:
            return self.set(self.frmt)

        return self

    def set(self, d):
        self.request.session[self.s] = d

        self.sess = d

        return self
        
    def _set(self):
        
        return self.set(self.sess)

    def setByName(self, name, s):

        self.sess[name] = s

        return self.set(self.sess)

    def clear(self):

        return self.set(self.frmt)