#coding:utf-8
from django.http import HttpResponse
import json

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

    def setByDict(self, d):

        return self.set(dict({ i: u'%s' % v for i,v in d.items() if i in self.frmt}))

    def setByName(self, name, s):
        self.sess[name] = s

        return self.set(self.sess)


    def clear(self):

        return self.set(self.frmt)



# JSON数据格式化类
class AjaxRJson:
    """
        统一全局JSON 字典格式化

        {
            error: False,
            msg: 'success',
            data: {},
        }

    """
    def __init__(self):
        self.error = False
        self.msg = 'success'
        self.data = {}

    def dumps(self, data=''):
        if data:
            self.data = data

        return HttpResponse(json.dumps({'err':self.error, 'msg':self.msg, 'data':self.data }))

    def message(self, msg = ''):
        
        self.msg = msg
        self.error = True

        return self