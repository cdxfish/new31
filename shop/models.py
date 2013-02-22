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
