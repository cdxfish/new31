#coding:utf-8
from django.db import models
from item.models import *

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=30,unique=True)

    def __unicode__(self):
        return u"%s" % self.tag

class ItemTag(models.Model):
    tag = models.ManyToManyField(Tag)
    name = models.ManyToManyField(Item)

    def __unicode__(self):
        return u"%s - %s" % (type(self.tag), self.tag.values)