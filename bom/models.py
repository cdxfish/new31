#coding:utf-8
from django.db import models
from order.models import *

# Create your models here.

class Produce(models.Model):
    chcs = (
            (0, u'未产'),
            (1, u'产中'),
            (2, u'拒产'), 
            (3, u'已产'), 
        )
    item = models.ForeignKey(OrderItem, verbose_name=u'商品')
    status = models.SmallIntegerField(u'生产状态', default=0, editable=False, choices=chcs)

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.item, self.status)