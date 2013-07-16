#coding:utf-8
from django.db import models

# Create your models here.

class PayManager(models.Manager):
    def getPayById(self, id = ''):

        return self.select_related().get(onl=True, id=id)
        
    def getDefault(self):

        return self.select_related().filter(onl=True)[0]

    def getTupleByAll(self):
        pay = self.filter(onl=True)

        a = [(i.id, i.name) for i in pay]

        return tuple(a)

class Pay(models.Model):
    name = models.CharField(u'名字', max_length=30)
    cod = models.CharField(u'代码', max_length=30)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    objects = PayManager()

    def __unicode__(self):
        return u"%s - %s" % (self.name, self.onl)

    # class Meta:
        # verbose_name = u'支付方式'