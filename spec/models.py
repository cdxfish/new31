#coding:utf-8
from django.db import models

# Create your models here.

class Spec(models.Model):
    value = models.CharField(u'规格', max_length=30, unique=True)

    def __unicode__(self):
        return u"%s" % self.value

    class Meta:
        ordering = ['value']