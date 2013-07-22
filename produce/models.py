#coding:utf-8
from django.db import models
from order.models import *

# Create your models here.

class proManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in Produce.act[i]])


class Produce(models.Model):
    chcs = (
            (0, u'未产'),
            (1, u'产求'),
            (2, u'产中'),
            (3, u'拒产'),
            (4, u'已产'),
        )

    act =   (
                ((1, u'产求'), ),
                ((2, u'产中'), (3, u'拒产'), ),
                ((3, u'拒签'), (4, u'已产'), ),
                ((1, u'产求'), ),
                (),
            )

    item = models.OneToOneField(OrdItem, verbose_name=u'商品')
    status = models.SmallIntegerField(u'生产状态', default=0, editable=False, choices=chcs)

    objects = proManager()

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.item, self.status)