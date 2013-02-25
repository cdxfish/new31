from django.db import models

# Create your models here.
class AttriBute(models.Model):
    attr = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.attr

class Discount(models.Model):
    discount = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.discount

class Ad(models.Model):
    url = models.CharField(max_length=60)
    img = models.CharField(max_length=60)
    show = models.BooleanField()
    vieworder = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.img

class Config(models.Model):
    code = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __unicode__(self):
        return u"%s" % self.code

class Logistics(models.Model):
    value = models.CharField(max_length=60)
    isOpen = models.BooleanField(max_length=60)
    vieworder = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.value

class Signature(models.Model):
    value = models.CharField(max_length=60)
    isOpen = models.BooleanField(max_length=60)
    vieworder = models.SmallIntegerField()
    limitNum = models.SmallIntegerField()

    def __unicode__(self):
        return u"%s" % self.value