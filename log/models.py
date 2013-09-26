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

    # chcs = (
    #         (0, u'新单'),
    #         (1, u'编辑'),
    #         (2, u'确认'),
    #         (3, u'取消'),
    #         (4, u'无效'),
    #         (5, u'完成'),
    #         (6, u'停止'),
    #         (7, u'发货'),
    #         (8, u'签收'),
    #         (9, u'拒签'),
    #         (10, u'付款'),
    #     )
    chcs = tuple((i[0],i[1]) for i in Element.pPath + Element.nPath)

    ord = models.ForeignKey(Ord, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户')
    # act = models.ForeignKey(Element, verbose_name=u'动作')
    # typ = models.SmallIntegerField(u'日志类型', default=0, choices=chcs)
    act = models.CharField(u'动作', max_length=60, choices=chcs)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    objects = logManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.ord, self.get_typ_display(), self.time )
        
    class Meta:
        unique_together=(("ord","time"),)
        # verbose_name = u'订单日志'
        # 记录类似于下单时间.付款时间.发货时间等