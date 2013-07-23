#coding:utf-8
from django.db import models

# Create your models here.

class proManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in Pro.act[i]])

    def getFeeBySN(self, sn):

        ord = Ord.objects.select_related().get(sn=sn)
        total = 0
        for i in ord.orditem_set.all():
            total += forMatFee(i.nfee * i.num)

        return total

class Pro(models.Model):
    from order.models import Ord
    from item.models import ItemFee
    from discount.models import Dis
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

    ord = models.ForeignKey(Ord, verbose_name=u'订单')
    name = models.CharField(u'商品', max_length=30)
    sn = models.CharField(u'货号', max_length=30)
    spec = models.CharField(u'规格', max_length=30)
    num = models.SmallIntegerField(u'数量')
    typ = models.SmallIntegerField(u'商品类型', default=0, choices=ItemFee.chcs)
    fee = models.DecimalField(u'原价', max_digits=10, decimal_places=2)
    nfee = models.DecimalField(u'现价', max_digits=10, decimal_places=2)
    dis = models.FloatField(u'折扣', default=1.0, choices=Dis.chcs)
    status = models.SmallIntegerField(u'生产状态', default=0, editable=False, choices=chcs)

    objects = proManager()

    def __unicode__(self):
        return u"%s - [ %s ]" % ( self.item, self.status)