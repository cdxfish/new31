#coding:utf-8
from django.db import models

# Create your models here.

class OrdLog(models.Model):
    from django.contrib.auth.models import User
    from order.models import Ord
    
    chcs = (
            (0, u'新单'),
            (1, u'编辑'),
            (2, u'确认'),
            (3, u'取消'),
            (4, u'无效'),
            (5, u'完成'),
            (6, u'停止'),
            (7, u'发货'),
            (8, u'签收'),
            (9, u'拒签'),
            (10, u'付款'),
        )

    ord = models.ForeignKey(Ord, verbose_name=u'订单')
    user = models.ForeignKey(User, verbose_name=u'用户')
    log = models.SmallIntegerField(u'日志类型', default=0, choices=chcs)
    note = models.CharField(u'备注', max_length=60, blank=True, null=True)
    time = models.DateTimeField(u'时间', auto_now=True, auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % ( self.ord, self.get_log_display(), self.time )
        
    class Meta:
        unique_together=(("ord","time"),)
        # verbose_name = u'订单日志'
        # 记录类似于下单时间.付款时间.发货时间等