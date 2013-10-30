#coding:utf-8
from django.db import models

# Create your models here.

class fncManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i[0] for i in Fnc.act[i]])


    def saveFnc(self, ord, request):
        from views import FncSess
        from payment.models import Pay

        try:
            fnc = ord.fnc
        except Exception, e:
            fnc = Fnc()

        fnc.ord = ord
        fnc.cod = FncSess(request).getObj()['pay']

        fnc.save()

        return self

    def cStatus(self, sn , s):
        fnc = self.get(ord=sn)

        fnc.status = s

        fnc.save()

        return fnc
        
    def stop(self, sn):

        return self.cStatus(sn, 4)

    def getAll(self):

        return self.select_related().filter(ord__status__gt=1)


class Fnc(models.Model):
    from order.models import Ord
    from payment.models import Pay

    _chcs = (
                (0, u'未付', 'finance:unpaidFnc'), 
                (1, u'已付', 'finance:paidFnc'),
                (2, u'已结', 'finance:closedFnc'),
                (3, u'已核', 'finance:checkedFnc'),
                (4, u'止付', 'finance:stopFnc'),
            )

    chcs= tuple((i[0],i[1]) for i in _chcs)

    act =   (
                (_chcs[0], _chcs[1], _chcs[4], ),
                (_chcs[0], _chcs[2], ),
                (_chcs[0], _chcs[3], ),
                (_chcs[0], ),
                (_chcs[0], ),
        )

    ord = models.OneToOneField(Ord, verbose_name=u'订单')
    cod = models.ForeignKey(Pay, verbose_name=u'支付方式')
    status = models.SmallIntegerField(u'支付状态', default=0, choices=chcs)

    objects = fncManager()

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.ord, self.cod.get_cod_display(), self.get_status_display() )

    # class Meta:
        # verbose_name = u'订单支付'