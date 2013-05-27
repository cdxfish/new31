#coding:utf-8

from django.db import models

# Create your models here.

class AreaManager(models.Manager):
    def getAreaById(self, id = ''):

        return self.select_related().get(onLine=True, id=id)

    def getDefault(self):

        return self.select_related().filter(onLine=True)[0].sub_set.filter(onLine=True)[0]

    def  getTupleByAll(self):
        area = self.filter(onLine=True,sub=None)

        a = []
        for i in area:
            for ii in i.sub_set.all():
                a.append((ii.id, '%s - %s' % (i.name, ii.name)))

        return tuple(a)

class Area(models.Model):
    name = models.CharField(u'区域', max_length=32, unique=True)
    onLine = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    objects = AreaManager()

    def __unicode__(self):
        return u"%s [ onLine: %s] - %s" % (self.name, self.onLine, self.sub)