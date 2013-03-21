#coding:utf-8
from django.db import models

# Create your models here.

class tagManager(models.Manager):
    def randomTag(self, num = 10):

        return self.order_by('?')[: num]

    def getByTag(self, tag = '', num = 10):

        return self.select_related().filter(tag=tag)[: num]


class Tag(models.Model):
    tag = models.CharField(u'标签', max_length=60,unique=True)
    objects = tagManager()

    def __unicode__(self):
        return u"%s" % self.tag

    class Meta:
        ordering = ['?']