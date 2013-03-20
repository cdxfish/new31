#coding:utf-8
from django.db import models
from item.models import *

# Create your models here.


class tagManager(models.Manager):
    def allTag(self):

        return self.select_related().all()

    def randomTag(self, num = 10):

        return self.select_related().order_by('?')[: num]

    def getByTag(self, tag = '', num = 10):

        return self.select_related().filter(tag__contains=tag)[: num]



class Tag(models.Model):
    tag = models.CharField(max_length=30,unique=True)
    itemName = models.ManyToManyField(Item)
    objects = tagManager()

    def __unicode__(self):
        return u"%s" % self.tag