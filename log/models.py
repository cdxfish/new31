#coding:utf-8
from django.db import models
from django.core.urlresolvers import resolve, reverse
# Create your models here.

class logManager(models.Manager):

    def saveLog(self, ord, request):
        log = OrdLog()

        log.ord = ord
        log.user = request.user

        log.act = resolve(request.path).view_name

        log.save()

class OrdLog(models.Model):
    from django.contrib.auth.models import User
    from order.models import Ord
    from purview.models import Element

    chcs = tuple((i[0],i[1]) for i in Element.pPath + Element.nPath)

    ord = models.ForeignKey(Ord, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户', blank=True, null=True)
    act = models.CharField(u'动作', max_length=60, choices=chcs)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    objects = logManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.ord, self.get_typ_display(), self.time )
        
    class Meta:
        unique_together=(("ord","time"),)
        # verbose_name = u'订单日志'
        # 记录类似于下单时间.付款时间.发货时间等



class AccountLog(models.Model):
    from django.contrib.auth.models import User

    user = models.ForeignKey(User, verbose_name=u'用户', related_name='userlog')
    act = models.ForeignKey(User, verbose_name=u'操作者', related_name='actlog')
    note = models.CharField(u'动作', max_length=1024)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)