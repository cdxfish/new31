# coding: UTF-8
from django.db import models
from django.core.urlresolvers import resolve, reverse
# Create your models here.

class ItemWeight(models.Model):
    from item.models import Item

    item = models.OneToOneField(Item, verbose_name=u'商品')
    wh = models.IntegerField(verbose_name=u'权重值', default=0)

    def __unicode__(self):
        return u"%s - %s" % (self.item.name, self.wh)

    class Meta:
        ordering = ['wh']
        verbose_name_plural = u'商品权重'
        # app_label = 'item'