from django.contrib import admin
from .models import Products,Customer,Cart,Payment,OrderPlaced,Warehouse
# Register your models here.

admin.site.register(Products)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Payment)
admin.site.register(OrderPlaced)
admin.site.register(Warehouse)