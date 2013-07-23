#coding:utf-8
from django.db import models

# Create your models here.

class fncManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in Fnc.act[i]])

class Fnc(models.Model):
    from order.models import Ord
    from payment.models import Pay
    chcs = (
                (0, u'未付'), 
                (1, u'已付'),
                (2, u'已结'),
                (3, u'已核'),
            )

    act =   (
                ((1, u'已付'),),
                ((2, u'已结'),),
                ((3, u'已核'),),
                (),
        )

    ord = models.OneToOneField(Ord, verbose_name=u'订单')
    cod = models.ForeignKey(Pay, verbose_name=u'支付方式')
    status = models.SmallIntegerField(u'支付状态', default=0, editable=False, choices=chcs)

    objects = fncManager()

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.ord, self.name, self.get_status_display() )

    # class Meta:
        # verbose_name = u'订单支付'