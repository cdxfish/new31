#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class AjaxRJson(object):
    def __init__(self, msg='success'):

        self.msg = msg
        self.typ = {
            'warning': 'warning',
            'error': 'error',
            'success': 'success',
            'info': 'info',
            'debug': 'debug',
            
        }
        self.data = {}

    def dump(self, data, typ, msg=''):
        self.data = data
        if msg: self.msg = msg

        return json.dumps({'msg':self.msg, 'typ': self.typ[typ], 'data':self.data })


    def dumps(self, data, typ='success'):

        return HttpResponse(self.dump(data, typ))

    def warning(self, **kwarg):

        return self.dumps(kwarg, 'warning')

    def error(self, **kwarg):

        return self.dumps(kwarg, 'error')

    def success(self, **kwarg):

        return self.dumps(kwarg, 'success')

    def info(self, **kwarg):

        return self.dumps(kwarg, 'info')

    def debug(self, **kwarg):

        return self.dumps(kwarg, 'debug')

  

class msgManager(models.Manager):
    def __init__(self, *arg, **kwarg):
        super(msgManager, self).__init__(*arg, **kwarg)
        self.typ = {
            'warning': 'warning',
            'error': 'error',
            'success': 'success',
            'info': 'info',
            'debug': 'debug',
            
        }

    def read(self, *ids):

        return self.filter(id__in=list(ids), read=False).update(read=True)

    def get(self, user):
        if type(user) == 'str':
            return self.filter(user__username=user, read=False)
        else:
            return self.filter(user=user, read=False)

    def dumps(self, typ, msg='', data=[]):
        self.msg = msg
        self.data = data

        return json.dumps({ 'typ': self.typ[typ], 'msg':self.msg, 'data':self.data })

    def push(self, user, **kwarg):

        Msg.objects.create(_data=self.dumps(**kwarg), user=user)

        return self

    def pushByPath(self, path, **kwarg):
        from purview.models import Element

        for i in Element.objects.getUserByPath(path=path):
            self.push(user=i, **kwarg)

        return self

    def pushToRole(self, *role, **kwarg):
        for i in User.objects.filter(role__role__in=list(role), role__onl=True):
            self.push(user=i, **kwarg)

        return self

    def warning(self, **kwarg):

        return self.push(typ='warning', **kwarg)

    def error(self, **kwarg):

        return self.push(typ='error', **kwarg)

    def success(self, **kwarg):

        return self.push(typ='success', **kwarg)

    def info(self, **kwarg):

        return self.push(typ='info', **kwarg)

    def debug(self, **kwarg):

        return self.push(typ='debug', **kwarg)


class Msg(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    read = models.BooleanField(u'已读', default=False)
    _data = models.CharField(u'数据', max_length=1024)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def data(self):
        return json.loads(self._data)

    objects = msgManager()


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.read, self.msg)

    class Meta:
        ordering = ['time']
        # verbose_name = u'消息推送'