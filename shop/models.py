from django.db import models

# Create your models here.
class AttriBute(models.Model):
    attr = models.CharField(max_length=30)

class Discount(models.Model):
    discount = models.CharField(max_length=30)



