#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class msgManager(models.Manager):
    
    def pushToUser(self, typ, msg, data, user):

        Msg.objects.create(typ=typ, msg=msg, _data=json.dumps(data), user=user)

        return self

    def push(self, typ, msg, data, path):
        from purview.models import Element

        for i in Element.objects.getUserByPath(path=path):
            self.pushToUser(typ=typ, msg=msg, data=data, user=i)

        return self

    def read(self, *ids):

        return self.filter(id__in=list(ids), read=False).update(read=True)

    def get(self, user):
        if type(user) == 'str':
            return self.filter(user__username=user, read=False)
        else:
            return self.filter(user=user, read=False)

    def warning(self, msg, data, path):
        return self.push(0, msg, data, path)

    def error(self, msg, data, path):
        return self.push(1, msg, data, path)

    def success(self, msg, data, path):
        return self.push(2, msg, data, path)

    def info(self, msg, data, path):
        return self.push(3, msg, data, path)

    def debug(self, msg, data, path):
        return self.push(4, msg, data, path)



class Msg(models.Model):

    chcs = ((0, u'warning'), (1, u'error'), (2, u'success'), (3, u'info'), (4, u'debug'),)

    user = models.ForeignKey(User, verbose_name=u'用户')
    read = models.BooleanField(u'已读', default=False)
    _data = models.CharField(u'数据', max_length=1024)
    msg = models.CharField(u'消息', max_length=1024)
    typ = models.SmallIntegerField(u'类型', default=0, choices=chcs)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def data(self):
        return json.loads(self._data)

    objects = msgManager()


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.read, self.msg)

    class Meta:
        ordering = ['time']
        # verbose_name = u'消息推送'