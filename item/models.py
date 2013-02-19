from django.db import models

# Create your models here.
class item(models.Model):
    name = models.CharField(max_length=30)
    sn = models.CharField(max_length=30)
    add_time = models.CharField(max_length=30)
    last_update = models.CharField(max_length=30)
    shelf = models.CharField(max_length=30)
    show = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    like = models.CharField(max_length=30)
    click = models.CharField(max_length=30)

class attr(models.Model):
    name = models.CharField(max_length=30)
    sn = models.CharField(max_length=30)
    add_time = models.CharField(max_length=30)
    last_update = models.CharField(max_length=30)
    shelf = models.CharField(max_length=30)
    show = models.CharField(max_length=30)
    desc = models.CharField(max_length=30)
    like = models.CharField(max_length=30)
    click = models.CharField(max_length=30)

class tag(models.Model):
    tag = models.CharField(max_length=30)
