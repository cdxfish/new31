#coding:utf-8
from django.db import models
from django.contrib.auth.models import User
import json
# Create your models here.


class msgManager(models.Manager):
    
    def push(self, user, msg):
        m = Msg()
        m.user = user
        m._msg = json.dumps(msg)
        m.save()

        return self



class Msg(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户')
    read = models.BooleanField(u'已读', default=False)
    _msg = models.CharField(u'数据', max_length=1024)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def msg(self):
        return json.loads(self._msg)

    objects = msgManager()


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.read, self._msg)

    class Meta:
        ordering = ['-time']
        # verbose_name = u'消息推送'