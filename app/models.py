from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
# Create your models here.
class Product(models.Model):
    prid=models.AutoField(primary_key=True)
    Product_Name = models.CharField(max_length=500)
    original_price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False) 
    Current_price = models.IntegerField(null=False)
    rating=models.IntegerField(null=False,default=0)
    Product_display =models.CharField(max_length=256, choices=[('All', 'All'), ('New_Arrival', 'New_Arrival'),('On_Sale','On_Sale'),('Upcoming_product', 'Upcoming_product')],default="")
    Intial_quantity = models.IntegerField(default=0)
    size_available = models.CharField(max_length=256,default="")
    Description = models.TextField()
    image = models.ImageField(upload_to="image/",default='')
    image2 = models.ImageField(upload_to="image/",default='')
    image3 = models.ImageField(upload_to="image/",default='')
    image4 = models.ImageField(upload_to="image/",default='')
    def __str__(self):
        return str(self.prid)

class Banner(models.Model):
    banid= models.AutoField(primary_key=True)
    image1 = models.ImageField(upload_to="image/",default='')
    image2 = models.ImageField(upload_to="image/",default='')
    image3 = models.ImageField(upload_to="image/",default='')
    def __str__(self):
        return str(self.banid)
class Checkout(models.Model):
    check_id = models.ForeignKey(User, on_delete=models.CASCADE)
    Product_id = models.CharField(max_length=9000)
    items = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    phone = models.CharField(max_length=90,default="")
    def __str__(self):
        return str(self.check_id)

