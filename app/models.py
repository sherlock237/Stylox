from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MyProfile(models.Model):
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    name = models.CharField(max_length = 100)
    address = models.TextField(null=True, blank=True)
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    def __str__(self):
        return "%s" % self.user


class Product(models.Model):
    prid=models.AutoField(primary_key=True)
    Product_Name = models.CharField(max_length=500)
    original_price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False) 
    Current_price = models.IntegerField(null=False)
    main_class=models.CharField(max_length=256, choices=[('Men', 'Men'), ('Women', 'Women'),('Both','Both')], default="Men")
    category=models.CharField(max_length=256, choices=[('Jeans', 'Jeans'), ('T-shirts', 'T-shirts'),('Chino','Chino'),
    ('Pants','Pants'),('Trousers','Trousers'),('Shirts','Shirts'),('Winters','Winters'),('Shorts','Shorts'),
    ('Socks','Socks'),('Belt','Belt'),('Wallet','Wallet'),('Shoes','Shoes'),('Mask','Mask'),('other_accessories','other_accessories')],default="other_accessories")
    Product_display =models.CharField(max_length=256, choices=[('All', 'All'), ('New_Arrival', 'New_Arrival'),('On_Sale','On_Sale'),('Upcoming_product', 'Upcoming_product')],default="All")
    is_available =models.CharField(max_length=256, choices=[('in_stock', 'in_stock'), ('out_of_stock', 'out_of_stock'),('currently_unavailable','currently_unavailable')],default="currently_unavailable")
    Intial_quantity = models.IntegerField(default=0)
    size_available = models.CharField(max_length=256, help_text = mark_safe(_(
            '<small style="color:red;font-size:10px;">Please enter multiple size seperated by comma for ex: S,XL,XXL,XXXL</small>'
        )),default="")
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
    check_id = models.ForeignKey(User, on_delete=models.CASCADE, null =True)
    Product_id = models.CharField(max_length=9000)
    items = models.CharField(max_length=5000)
    fname = models.CharField(max_length=90, default="")
    lname = models.CharField(max_length=90, default="")
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90)
    phone = models.CharField(max_length=90,default="")
    add_info = models.CharField(max_length=1000, default="")
    company = models.CharField(max_length=200, default="")

    def get_absolute_url(self):
        return('/')

    def __str__(self):
        return str(self.check_id)

class Wishlist(models.Model):
    current_user = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    product = models.ForeignKey(to=Product, on_delete=CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "%s" % self.current_user

class Subscribe(models.Model):
    id= models.AutoField(primary_key=True)
    email = models.CharField(max_length=90)
    our_user=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
