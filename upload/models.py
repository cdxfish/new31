#coding:utf-8
from django.db import models

# Create your models here.

class imageManager(models.Manager):
    def getAll(self):

        return self.filter(onl=True)
        
class Image(models.Model):
    url = models.CharField(u'链接地址', max_length=120)
    img = models.ImageField(u'图片', upload_to='upload')
    onl = models.BooleanField(u'上线', default=True)
    sort = models.SmallIntegerField(u'排序', default=99)
    objects = imageManager()

    def __unicode__(self):
        return u"%s" %  self.img

    class Meta:
        ordering = ['sort']
        unique_together=(("img"),)  