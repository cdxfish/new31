# coding: UTF-8
from django.db import models

# Create your models here.

class Article(models.Model):

    tag = models.CharField(u'标签', max_length=30)
    title = models.CharField(u'标题', max_length=30)
    content = models.TextField(u'正文')
    onl = models.BooleanField(u'上线', default=True)

    def __unicode__(self):
        return u"%s - %s [ onl: %s ]" % (self.title, self.tag, self.onl)

    class Meta:
        verbose_name = u'文章'