from django.db import models
from users.models import User
# Create your models here.


class Partner(models.Model):
    partner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    shop_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    address_line_1 = models.TextField(max_length=100, blank=True, null=True)
    address_line_2 = models.TextField(max_length=100, blank=True, null=True)
    city_town = models.TextField(max_length=35, blank=True, null=True)
    province_region_state = models.TextField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.partner


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=20)
    mrp = models.DecimalField(max_digits=6, decimal_places=2)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    available = models.IntegerField()
    selling_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image_url = models.TextField(max_length=2500, default='NA')

    def __str__(self):
        return self.available