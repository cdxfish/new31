from django.db import models

# Create your models here.

class cart(models.Model):
    item = models.CharField(max_length=100)
    # type = models.ManyToManyField(type)
    # who = models.ForeignKey(who)