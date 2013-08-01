#coding:utf-8
from django.db import models

# Create your models here.

class proManager(models.Manager):
    def getActTuple(self, i):

        return tuple([ i for i, v in Pro.act[i]])

    def getFeeBySN(self, sn):
        from new31.func import frMtFee

        total = 0
        for i in self.select_related().filter(ord=sn):
            total += i.total()

        return total

    def savePro(self, ord, request):
        from cart.views import CartSess
        from item.models import Item, ItemSpec, ItemFee
        from discount.models import Dis
        from new31.func import frMtFee
        from decimal import Decimal

        items  = CartSess(request).sess

        _items = []

        for v,i in items.items():

            item = Item.objects.getByID(id=i['itemID'])
            spec = ItemSpec.objects.getBySid(id=i['specID'])
            fee = ItemFee.objects.getBySid(id=i['specID'])
            dis = Dis.objects.getByid(id=i['disID'])
            nfee = frMtFee(fee.fee * Decimal(dis.dis))

            _items.append(
                Pro(
                    ord=ord,
                    name=item.name,
                    sn=item.sn,
                    spec=spec.spec.value,
                    num=i['num'],
                    dis=dis.dis,
                    fee=fee.fee,
                    nfee=nfee,
                    )
                )

        Pro.objects.bulk_create(_items)

    def cStatus(self, pid , s):
        pro = self.get(id=pid)

        pro.status = s

        pro.save()


class Pro(models.Model):
    from order.models import Ord
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

    fee = models.DecimalField(u'原价', max_digits=10, decimal_places=2)
    nfee = models.DecimalField(u'现价', max_digits=10, decimal_places=2)
    dis = models.FloatField(u'折扣', default=1.0, choices=Dis.chcs)
    status = models.SmallIntegerField(u'生产状态', default=0, editable=False, choices=chcs)

    objects = proManager()

    def total(self):
        from new31.func import frMtFee

        return frMtFee(self.nfee * self.num)

    def __unicode__(self):
        return u"%s - %s [ %s ]" % ( self.name, self.spec, self.status)