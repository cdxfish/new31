#coding:utf-8
from django.db import models
import datetime

# Create your models here.
class invProManager(models.Manager):
    def cOnl(self, sid):
        try:
            invpro = self.select_related().get(spec__id=sid, spec__onl=True)
            
        except Exception, e:
            from item.models import ItemSpec

            invpro = InvPro()
            invpro.spec = ItemSpec.objects.get(id=sid)
            invpro.save()

        invpro.onl = False if invpro.onl else True
        invpro.save()

    def getAll(self):

        return self.select_related().filter(onl=True)


class invNumManager(models.Manager):
    def default(self):
        from produce.models import Pro

        d = datetime.date.today()
        t = d - datetime.timedelta(days=1)

        self.filter(date=d).delete()

        for i in InvPro.objects.getAll():
            lNum = Pro.objects.filter(sn=i.spec.item.sn, spec=i.spec.spec.value, ord__logcs__date=t).values('num')
            try:
                num = self.get(pro__spec__item__sn=i.spec.item.sn, pro__spec__spec__value=i.spec.spec.value, date=t).values('num')
            except Exception, e:
                num = [{'num':  0}]

            iNum = InvNum()
            iNum.pro = i
            iNum.date = d
            iNum.num = sum([v['num'] for v in num]) - sum([v['num'] for v in lNum])
            iNum.save()


    def getAll(self):
        from produce.models import Pro

        today = datetime.date.today()

        pros = InvPro.objects.getAll()

        for i in pros:
            i.invnum = []
            for ii in i.invnum_set.filter(date=today):
                l = sum([v['num'] for v in Pro.objects.filter(sn=i.spec.item.sn, spec=i.spec.spec.value, ord__logcs__date=today).values('num')])
                ii.count = ii.num - l
                ii.logcs = l
                i.invnum.append(ii)

        return pros


class InvPro(models.Model):
    from item.models import ItemSpec

    chcs =  (
            (False, u'不备'),
            (True, u'已备'),
        )

    spec = models.OneToOneField(ItemSpec, verbose_name=u'商品规格')
    onl = models.BooleanField(u'备货', default=False, choices=chcs)

    objects = invProManager()

    def __unicode__(self):
        return u"%s - %s" % (self.spec, self.get_onl_display())

class InvNum(models.Model):

    pro = models.ForeignKey(InvPro, verbose_name=u'备货清单')
    date = models.DateField(u'收货日期')
    num = models.SmallIntegerField(u'数量', default=0)

    objects = invNumManager()

    def __unicode__(self):
        return u'%s - [ date: %s ] [ num: %s ]' % (self.pro, self.date, self.num)

    class Meta:
        unique_together=(('pro','date'),)     