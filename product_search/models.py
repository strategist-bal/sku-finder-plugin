from django.db import models
from partner_inventory.models import User

# Create your models here.


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address_line_1 = models.TextField(max_length=150)
    address_line_2 = models.TextField(max_length=150)
    address_line_3 = models.TextField(max_length=150)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.customer
