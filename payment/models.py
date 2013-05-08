#coding:utf-8
from django.db import models

# Create your models here.



class PayManager(models.Manager):
    def getPayById(self, id = ''):

        pay = Pay.objects.select_related().get(id=id)

        if pay.onLine:

            return pay
        else:
            raise self.DoesNotExist

    def  getAll(self):
        pay = Pay.objects.filter(onLine=True)

        a = []
        for i in pay:
            a.append((i.id, i.name))

        return tuple(a)

class Pay(models.Model):
    name = models.CharField(u'名字', max_length=30)
    cod = models.CharField(u'代码', max_length=30)
    config = models.TextField(u'配置')
    onLine = models.BooleanField(u'上线')

    objects = PayManager()

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.onLine)

    # class Meta:
        # verbose_name = u'支付方式'