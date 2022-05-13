from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=20)
    mrp = models.IntegerField()

    def __str__(self):
        return self.name


class Partner(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(widget=forms.PasswordInput)
    dob = models.DateField()
    shop_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    address_line_1 = models.TextField(max_length=150)
    address_line_2 = models.TextField(max_length=150)
    address_line_3 = models.TextField(max_length=150)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.username


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    available = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.available
