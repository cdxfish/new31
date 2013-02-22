from django.db import models
from item.models import *

# Create your models here.

class Tag(models.Model):
    tag = models.CharField(max_length=30)

class ItemTag(models.Model):
    tag = models.ManyToManyField(Tag)
    name = models.ManyToManyField(Item)