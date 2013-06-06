#coding:utf-8
from django.db import models


# Create your models here.

class disManager(models.Manager):
    def getDefault(self):

        return self.get(discount=1)

    def getTupleByAll(self):

        return ((i.id, i.get_discount_display()) for i in  self.filter(onLine=True))

    def getDisByDisID(self,id):

        return  self.get(onLine=True,id=id)

    
class Discount(models.Model):
    disChoices = (
            (1.0, u'不打折'),
            (0.95, u'9.5 折'),
            (0.9, u'9.0 折'),
            (0.88, u'8.8 折'),
            (0.85, u'8.5 折'),
            (0.8, u'8.0 折'),
            (0.75, u'7.5 折'),
            (0.7, u'7.0 折'),
            (0.65, u'6.5 折'),
            (0.6, u'6.0 折'),
            (0.55, u'5.5 折'),
            (0.5, u'5.0 折'),
            (0.45, u'4.5 折'),
            (0.4, u'4.0 折'),
            (0.35, u'3.5 折'),
            (0.3, u'3.0 折'),
            (0.25, u'2.5 折'),
            (0.2, u'2.0 折'),
            (0.15, u'1.5 折'),
            (0.1, u'1.0 折'),
            (0.05, u'0.5 折'),
            # (0.0, u'赠送'),
        )
    discount = models.FloatField(u'折扣', default=1.0, choices=disChoices)
    onLine = models.BooleanField(u'上架', default=False)

    objects = disManager()

    def __unicode__(self):
        return u"%s" % self.get_discount_display()