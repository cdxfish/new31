#coding:utf-8

from django.db import models

# Create your models here.

class Discount(models.Model):
    discount = models.DecimalField(u'折扣', max_digits=3, decimal_places=1)

    def __unicode__(self):
        return u"%s" % self.discount