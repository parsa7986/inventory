from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CITY_CHOICES=(
    ('Tehran','Tehran'),
    ('Shiraz','Shiraz'),
    ('Isfahan','Isfahan'),
    ('Tabriz','Tabriz'),
    ('Mashhad','Mashhad'),
)

CATEGORY_CHOICES=(
    ('PS','Pistachio'),
    ('AL','Almond'),
    ('WL','Walnut'),
    ('HZ','Hazelnut'),
    ('DA','Dates'),
)

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    
class Products(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    description=models.TextField()
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image=models.ImageField(upload_to='product')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(choices=CITY_CHOICES,max_length=50)    
    mobile = models.IntegerField(default=0)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

STATUS_CHOICES=(
    ('Accepted','Accepted'),
    ('pending','pending'),
    ('delivered','delivered'),
    ('on the way','on the way'),
    ('packed','packed'),
)    

class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    order_id = models.CharField(max_length=100,blank=True,null=True)
    payment_status = models.CharField(max_length=100,blank=True,null=True)
    payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=True)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default='')
    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

