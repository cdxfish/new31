#coding:utf-8
from django.db import models

# Create your models here.

class tagManager(models.Manager):
    def getRandom(self):

        return self.filter(onl=True).order_by('?')[0]

    def getTagByTagTitle(self, tag = ''):

        return self.select_related().get(tag=tag, onl=True)

    def getTagByAll(self):

        return self.select_related().filter(onl=True)

class Tag(models.Model):
    
    tag = models.CharField(u'标签', max_length=60, unique=True)
    onl = models.BooleanField(u'上线', default=True)
    objects = tagManager()

    def __unicode__(self):
        return u"%s [ onl: %s ]" % (self.tag, self.onl)

    class Meta:
        ordering = ['?']