#coding:utf-8
from django.db import models

# Create your models here.
        
class Image(models.Model):
    value = models.ImageField(u'图片', upload_to='images',null=True,blank=True)

    def __unicode__(self):
        return u"%s" % self.value