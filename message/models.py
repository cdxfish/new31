#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.

class msgManager(models.Manager):
    
    def push(self, msg, user):

        Msg.objects.create(_data=json.dumps(msg), user=user)

        return self

    def pushs(self, msg, *role):

        for i in User.objects.filter(role__role__in=list(role), role__onl=True):
            Msg.objects.create(_data=json.dumps(msg), user=i)

        return self

    def read(self, *ids):

        return self.filter(id__in=list(ids), read=False).update(read=True)

    def get(self, user):
        if type(user) == 'str':
            return self.filter(user__username=user, read=False)
        else:
            return self.filter(user=user, read=False)

    def success(self):
        pass
    def debug(self):
        pass
    def info(self):
        pass
    def warning(self):
        pass
    def error(self):
        pass



class Msg(models.Model):

    chcs = ((0, u'warning'), (1, u'error'), (2, u'success'), (3, u'info'), (4, u'debug'),)

    user = models.ForeignKey(User, verbose_name=u'用户')
    read = models.BooleanField(u'已读', default=False)
    _data = models.CharField(u'数据', max_length=1024)
    typ = models.SmallIntegerField(u'类型', default=0, choices=chcs)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def data(self):
        return json.loads(self._data)

    objects = msgManager()


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.read, self._data)

    class Meta:
        ordering = ['time']
        # verbose_name = u'消息推送'