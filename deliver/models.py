#coding:utf-8
from django.db import models

# Create your models here.

class dlvrManager(models.Manager):
    def getDlvrById(self, id = ''):

        return self.select_related().get(onl=True, id=id)
        
    def getDefault(self):

        return self.select_related().filter(onl=True)[0]

    def getTupleByAll(self):

        return tuple([(i.id, i.get_cod_display()) for i in self.filter(onl=True)])

class Deliver(models.Model):
    chcs = (
                ('cod', u'市区内免费送货上门'), 
        )

    cod = models.CharField(u'代码', max_length=30, choices=chcs)
    config = models.TextField(u'配置')
    onl = models.BooleanField(u'上线')

    objects = dlvrManager()

    def __unicode__(self):
        return u"%s - %s" % (self.get_cod_display(), self.onl)

    # class Meta:
        # verbose_name = u'支付方式'