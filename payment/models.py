#coding:utf-8
from django.db import models

# Create your models here.

class PayManager(models.Manager):
    def getPayById(self, id = ''):

        return self.select_related().get(onLine=True, id=id)
        
    def getDefault(self):

        return self.select_related().filter(onLine=True)[0]

    def getTupleByAll(self):
        pay = self.filter(onLine=True)

        a = [(i.id, i.name) for i in pay]

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