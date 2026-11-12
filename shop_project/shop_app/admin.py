from django.contrib import admin

# Register your models here.
from .models import (
    Age, AnimalSubtype, AnimalType, Category, Manufacturer, Order, OrderItem,
    OrderStatus, PaymentMethod, PickupPoint, Product, Review, Size,
)

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Age)
admin.site.register(Size)
admin.site.register(AnimalType)
admin.site.register(AnimalSubtype)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(PaymentMethod)
admin.site.register(OrderStatus)
admin.site.register(PickupPoint)
admin.site.register(Order)
admin.site.register(OrderItem)