# coding: UTF-8
from django.db import models

# Create your models here.

class dlvrManager(models.Manager):
    def getDlvrById(self, id = ''):

        return self.select_related().get(onl=True, id=id)

    def default(self):

        return self.select_related().filter(onl=True)[0]

    def getTpl(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter(onl=True)])

class Deliver(models.Model):
    import api

    chcs = tuple( [ (i, api.__dict__[i].__doc__, ) for i in dir(api) if i[0] != '_' ] )

    cod = models.CharField(u'代码', max_length=30, choices=chcs)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    objects = dlvrManager()

    def __unicode__(self):
        return u"%s - %s" % (self.get_cod_display(), self.onl)

    class Meta:
        verbose_name_plural = u'物流方式'