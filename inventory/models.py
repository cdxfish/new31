#coding:utf-8
from django.db import models
from new31.func import frmtDate
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
    def default(self, date=''):
        if date:
            date = frmtDate(date)
        else:
            date = datetime.date.today()

        t = date - datetime.timedelta(days=1)

        self.filter(date=date).delete()

        for i in InvPro.objects.getAll():

            self.frMt(i.id, date)
            

    def frMt(self, id, date):
        from produce.models import Pro

        t = date - datetime.timedelta(days=1)

        pro = InvPro.objects.get(id=id)

        adv = Pro.objects.filter(sn=pro.spec.item.sn, spec=pro.spec.spec.value, ord__logcs__date=t).values('num')
        try:
            num = self.get(pro__spec__item__sn=pro.spec.item.sn, pro__spec__spec__value=pro.spec.spec.value, date=t).num
        except Exception, e:
            num = 0

        iNum = InvNum()
        iNum.pro = pro
        iNum.date = date
        iNum.num = num - sum([v['num'] for v in adv])
        iNum.save()

        return iNum


    def getAll(self, date):
        from produce.models import Pro
        if date:
            date = frmtDate(date)
        else:
            date = datetime.date.today()

        pros = InvPro.objects.getAll()

        for i in pros:
            adv = sum([v['num'] for v in Pro.objects.filter(sn=i.spec.item.sn, spec=i.spec.spec.value, ord__logcs__date=date).values('num')])
            try:
                invnum = i.invnum_set.get(date=date)
            except Exception, e:
                invnum = self.frMt(i.id, date)
            invnum.adv = adv
            invnum.count = invnum.num - adv

            i.invnum = invnum

        return pros

    def minus(self, id):

        num = self.get(id=id)
        num.num -= 1

        num.save()

    def plus(self, id):

        num = self.get(id=id)
        num.num += 1

        num.save()


class InvPro(models.Model):
    from item.models import ItemSpec

    chcs =  (
            (False, u'不备'),
            (True, u'已备'),
        )

    typ = (
            ('minus', u'减'),
            ('plus', u'加'),
        )
    act =   (
                (('minus', u'减'),('plus', u'加'),),
                (('minus', u'减'),('plus', u'加'),),
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