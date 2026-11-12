from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AnimalType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AnimalSubtype(models.Model):
    animal_type = models.ForeignKey(AnimalType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.animal_type.name + ' - ' + self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=300, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.IntegerField()
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    age = models.ForeignKey(Age, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    subtypes = models.ManyToManyField(AnimalSubtype, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name + ' - ' + str(self.rating)


class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class PickupPoint(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name + ', ' + self.address


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_point = models.ForeignKey(PickupPoint, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Заказ ' + str(self.id)

    def total(self):
        result = 0
        for item in self.items.all():
            result += item.price * item.quantity
        return result


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name
