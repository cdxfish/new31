#coding:utf-8
from django.db import models
# Create your models here.


class msgManager(models.Manager):
    pass



class Msg(models.Model):
    user = models.ForeignKey(User, verbose_name=u'用户', blank=True, null=True)
    msg = models.CharField(u'动作', max_length=60, choices=chcs)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    objects = msgManager()


    def __unicode__(self):
        return u"%s [ %s ] - %s" % (self.user, self.msg)

    class Meta:
        ordering = ['-time']
        # verbose_name = u'消息推送'