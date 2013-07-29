#coding:utf-8

from django.db import models

# Create your models here.

class AreaManager(models.Manager):
    def getAreaById(self, id = ''):

        return self.select_related().get(onl=True, id=id)

    def default(self):

        return self.select_related().filter(onl=True)[0].sub_set.filter(onl=True)[0]

    def getTpl(self):
        area = self.filter(onl=True,sub=None)

        return tuple( [(ii.id, '%s - %s' % (i.name, ii.name)) for i in area for ii in i.sub_set.all()] )

class Area(models.Model):
    name = models.CharField(u'区域', max_length=32, unique=True)
    onl = models.BooleanField(u'上线', default=True)
    sub = models.ForeignKey("self",related_name='sub_set', verbose_name=u'从属', blank=True, null=True)

    objects = AreaManager()

    def __unicode__(self):
        return u"%s [ onl: %s] - %s" % (self.name, self.onl, self.sub)