#coding:utf-8
from django.db import models
from item.models import *

# Create your models here.


class tagManager(models.Manager):
    def count(self, keyword):
        return self.filter(title__icontains=keyword).count()
        
    def allTag(self):
        return self.all()

class Tag(models.Model):
    tag = models.CharField(max_length=30,unique=True)
    item = models.ManyToManyField(Item)
    objects = tagManager()

    def __unicode__(self):
        return u"%s" % self.tag