#coding:utf-8
from django.db import models
from item.models import *

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=30,unique=True)

    def __unicode__(self):
        return u"%s" % self.tag

class ItemTag(models.Model):
    tag = models.ForeignKey(Tag)
    item = models.ForeignKey(Item)

    def __unicode__(self):
        return u"%s - %s" % (self.tag, self.item)

    class Meta:
    	ordering = ['tag','item']
        unique_together=(("tag","item"),)           