#coding:utf-8
from django.db import models

# Create your models here.

class tagManager(models.Manager):
    def getRandom(self, num = 10):

        return self.filter(onLine=True).order_by('?')[: num]

    def getTagByTagTitle(self, tag = ''):

        return self.select_related().get(tag=tag, onLine=True)

class Tag(models.Model):
    tag = models.CharField(u'标签', max_length=60, unique=True)
    onLine = models.BooleanField(u'上线', default=True)
    objects = tagManager()

    def __unicode__(self):
        return u"%s [ onLine: %s ]" % (self.tag, self.onLine)

    class Meta:
        ordering = ['?']