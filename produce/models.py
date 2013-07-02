#coding:utf-8
from django.db import models
from order.models import *

# Create your models here.

class Produce(models.Model):
    oStatus = (
            (0, u'未产'),
            (1, u'产求'),
            (2, u'产中'),
            (3, u'拒产'),
            (4, u'已产'),
        )
    item = models.OneToOneField(OrderItem, verbose_name=u'商品')
    status = models.SmallIntegerField(u'生产状态', default=0, editable=False, choices=oStatus)

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.item, self.status)