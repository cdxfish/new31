#coding:utf-8
from django.http import HttpResponse
import json, datetime

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

        return self.set(dict({ i[0]: u'%s' % i[1] for i in d.items() if i[0] in self.frmt}))

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
        
        self.data = data if data else ''

        return HttpResponse(json.dumps({'err':self.error, 'msg':self.msg, 'data':self.data }))

    def err(self, msg = ''):
        
        self.msg = msg
        self.error = True

        return self.dumps()




"""
tzinfo是关于时区信息的类
tzinfo是一个抽象类，所以不能直接被实例化
"""
class UTC(datetime.tzinfo):
    """UTC"""
    def __init__(self,offset = 0):
        self._offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return datetime.timedelta(hours=self._offset)