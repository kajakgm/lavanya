from django.db import models
import os
import datetime
from django.contrib.auth.models import User
def getFileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

# Create your models here.
class Catagory(models.Model):

    name=models.CharField(max_length=150,blank=False,null=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=200)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Products(models.Model):
    category=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,blank=False,null=False)
    vendor=models.CharField(max_length=150,blank=False,null=False)
    product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    qty=models.IntegerField(null=False,blank=False)
    original_price=models.FloatField(null=False)
    selling_price=models.FloatField(blank=False)
    description=models.TextField(max_length=200)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)
class cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.product_qty*self.product.selling_price
class Favourite(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)