#coding:utf-8
from django.db import models

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

class invNumManager(models.Manager):
    def default(self, sid):
        try:
            invpro = self.select_related().get(spec__id=sid, spec__onl=True)
            
        except Exception, e:
            from item.models import ItemSpec

            invpro = InvPro()
            invpro.spec = ItemSpec.objects.get(id=sid)
            invpro.save()

        invpro.onl = False if invpro.onl else True
        invpro.save()


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
    num = models.SmallIntegerField(u'数量')

    objects = invNumManager()

    def __unicode__(self):
        return u'%s - [ date: %s ] [ num: %s ]' % (self.pro, self.date, self.num)

    class Meta:
        unique_together=(('pro','date'),)     