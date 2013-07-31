#coding:utf-8
from django.db import models

# Create your models here.

class fncManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in Fnc.act[i]])


    def saveFnc(self, ord, request):
        from views import FncSess
        try:
            fnc = ord.fnc
        except Exception, e:
            fnc = Fnc()

        fnc.ord = ord
        fnc.cod = FncSess(request).getObj()['pay']

        fnc.save()

    def cStatus(self, sn , s):
        fnc = self.get(ord=sn)

        fnc.status = s

        fnc.save()
        
    def stop(self, sn):

        return self.cStatus(sn, 4)


class Fnc(models.Model):
    from order.models import Ord
    from payment.models import Pay
    chcs = (
                (0, u'未付'), 
                (1, u'已付'),
                (2, u'已结'),
                (3, u'已核'),
                (4, u'止付'),
            )

    act =   (
                ((1, u'已付'),(4, u'止付'),),
                ((2, u'已结'),),
                ((3, u'已核'),),
                (),
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