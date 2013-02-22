from django.db import models

# Create your models here.
class AttriBute(models.Model):
    attr = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.attr

class Discount(models.Model):
    discount = models.CharField(max_length=30)

class Ad(models.Model):
    url = models.CharField(max_length=60)
    img = models.CharField(max_length=60)
    show = models.BooleanField()
    vieworder = models.IntegerField()

class Config(models.Model):
    code = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.discount