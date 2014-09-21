# coding: UTF-8
from django.db import models
from new31.func import frmtDate
from area.models import Area
import datetime

# Create your models here.

class buildManager(models.Manager):

    def getAll(self):

        return self.select_related().filter(onl=True)

    def addPro(self, sid):

        return

    def rePro(self, sid):

        return

    def getByUser(self, user):

        return self.getAll().filter(area__name__in=user.attribution_set.getAreaList()).distinct()

class invProManager(models.Manager):
    def cOnl(self, sid):
        invpro = self.get(id=sid)
        invpro.onl = False if invpro.onl else True
        invpro.save()

        return invpro


    def getAll(self):

        return self.select_related().filter(onl=True)

    def hasPro(self, bid, sid):

        try:
            pro = self.get(build__id=bid, spec__id=sid)

            return pro.onl

        except Exception, e:
            # raise e
            return False

    def cPro(self, bid, sid):

        try:
            pro = self.get(build__id=bid, spec__id=sid)


            pro.onl = False if pro.onl else True
            pro.save()

            return pro.onl

        except Exception, e:
            from item.models import ItemSpec
            # raise e

            pro = InvPro()
            pro.build = Build.objects.get(id=bid)
            pro.spec = ItemSpec.objects.get(id=sid)
            pro.onl = True

            pro.save()

            return True


class invNumManager(models.Manager):
    def default(self, user, date):
        if date:
            date = frmtDate(date)
        else:
            date = datetime.date.today()

        t = date - datetime.timedelta(days=1)

        self.filter(date=date).delete()

        for i in InvPro.objects.getAll().filter(build__area__name__in=user.attribution_set.getAreaList()).distinct():

            self.frMt(i, date)

    def frMt(self, pro, date):
        from produce.models import Pro

        inum = InvNum()
        inum.pro = pro
        inum.date = date

        try:
            t = date - datetime.timedelta(days=1)

            _inum = self.get(pro=pro, date=t)
            inum.num = _inum.count
        except Exception, e:
            # raise e
            inum.num = 0

        inum.save()

        return inum


    def getAll(self, date):
        from produce.models import Pro
        from area.models import Area

        if date:
            date = frmtDate(date)
        else:
            date = datetime.date.today()


        return self.select_related().filter(pro__onl=True, date=date)

    def minus(self, sn, num=1):
        inv = self.get(id=sn)
        inv.num -= num
        inv.count -= num

        inv.save()

        return inv

    def plus(self, sn, num=1):
        inv = self.get(id=sn)
        inv.num += num
        inv.count += num

        inv.save()

        return inv

class Build(models.Model):

    chcs = (
            (0, u'南宁'),
            (1, u'长沙'),
        )

    name = models.SmallIntegerField(u'厂房', default=0, choices=chcs)
    area = models.ManyToManyField(Area, verbose_name=u'供货区域', blank=True, null=True)
    onl = models.BooleanField(u'上线', default=True)

    objects = buildManager()

    def __unicode__(self):
        return u'%s - [ onl: %s ]' % (self.get_name_display(), self.onl)

    class Meta:
        verbose_name_plural = u'厂房'


class InvPro(models.Model):
    from item.models import ItemSpec

    chcs =  (
            (False, u'不备'),
            (True, u'已备'),
        )

    spec = models.ForeignKey(ItemSpec, verbose_name=u'商品规格')
    build = models.ForeignKey(Build, verbose_name=u'厂房')
    onl = models.BooleanField(u'备货', default=False, choices=chcs)

    def _onl(self):


        return self.onl

    objects = invProManager()

    def __unicode__(self):
        return u"%s - [ %s ][ %s ]" % (self.spec,  self.get_onl_display(), self.build.get_name_display())

    class Meta:
        verbose_name_plural = u'备货清单'


class InvNum(models.Model):
    _typ = (
            (0, u'减', 'inventory:minusInv'),
            (1, u'加', 'inventory:plusInv'),
        )

    typ = tuple((i[0],i[1]) for i in _typ)
    act = (_typ[0], _typ[1], )

    pro = models.ForeignKey(InvPro, verbose_name=u'备货清单')
    date = models.DateField(u'收货日期')
    num = models.SmallIntegerField(u'数量', default=0)

    def __init__(self, *arg, **kwarg):
        from produce.models import Pro
        from order.models import Ord
        super(InvNum, self).__init__(*arg, **kwarg)

        try:
            adv = Pro.objects.filter(
                    ord__status=Ord.chcs[2][0],
                    ord__logcs__date=self.date,
                    ord__logcs__area__in=[ i.get_name_display() for i in self.pro.build.area.all()],
                    spec=self.pro.spec.spec.value,
                    name=self.pro.spec.item.name
                ).aggregate(models.Sum('num'))['num__sum']
        except Exception, e:
            # raise e
            adv = 0

        self.adv = adv if adv else 0
        self.count = self.num - self.adv

    objects = invNumManager()

    def __unicode__(self):
        return u'%s - [ date: %s ] [ num: %s ]' % (self.pro, self.date, self.num)

    class Meta:
        unique_together=(('pro','date'),)
        verbose_name_plural = u'备货量'
        ordering = ['pro__build', 'pro__spec',]
