#coding:utf-8
from django.db import models


# Create your models here.

class disManager(models.Manager):
    def default(self):

        return self.get(dis=1)

    def getTpl(self):

        return ((i.id, i.get_dis_display()) for i in  self.filter(onl=True))

    def getByid(self, id):

        return self.get(onl=True,id=id)

    def getBySid(self, id):

        return self.select_related().get(itemfee__spec__id=id, itemfee__typ=0, onl=True)

    
class Dis(models.Model):
    chcs = (
            (1.0, u'原价'),
            (0.95, u'9.5 折'),
            (0.9, u'9.0 折'),
            (0.88, u'8.8 折'),
            (0.85, u'8.5 折'),
            (0.8, u'8.0 折'),
            (0.795, u'7.95 折'),
            (0.77, u'7.7 折'),
            (0.752, u'7.52 折'),
            (0.75, u'7.5 折'),
            (0.7, u'7.0 折'),
            (0.66, u'6.6 折'),
            (0.65, u'6.5 折'),
            (0.6, u'6.0 折'),
            (0.55, u'5.5 折'),
            (0.53, u'5.3 折'),
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
            (0.0, u'赠送'),
        )
    dis = models.FloatField(u'折扣', default=1.0, choices=chcs)
    onl = models.BooleanField(u'上架', default=False)

    objects = disManager()

    def __unicode__(self):
        return u"%s" % self.get_dis_display()

    class Meta:
        ordering = ['-dis']