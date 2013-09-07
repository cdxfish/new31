#coding:utf-8
from django.db import models

# Create your models here.

class PayManager(models.Manager):
    def getPayById(self, id = ''):

        return self.select_related().get(onl=True, id=id)
        
    def default(self):

        return self.select_related().filter(onl=True)[0]

    def getTpl(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter(onl=True)])

    def getTplToShow(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter((models.Q(cod='payafter') | models.Q(cod='alipay') | models.Q(cod='post') ), onl=True)])

class Pay(models.Model):
    chcs = (
                ('payafter', u'货到付款'),
                ('alipay', u'支付宝'),
                ('post', u'货到付款 ( 刷卡 )'),
                ('quarter', u'季结'),
                ('monthly', u'月结'),
                ('weekly', u'周结'),
        )

    cod = models.CharField(u'代码', max_length=30, choices=chcs)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    objects = PayManager()

    def __unicode__(self):
        return u"%s - %s" % (self.cod, self.onl)

    # class Meta:
        # verbose_name = u'支付方式'