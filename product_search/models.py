from django.db import models
from partner_inventory.models import User#, Listing

# Create your models here.


class Customer(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    current_latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    current_longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.customer


class Address(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    default_address = models.BooleanField('partner status', default=False)
    address_line_1 = models.TextField(max_length=150)
    address_line_2 = models.TextField(max_length=150)
    address_line_3 = models.TextField(max_length=150)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)


# class Cart(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
#     quantity = models.IntegetField()
#     is_current = 1
#
# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     cart = models.ForeignKey(Customer, on_delete=Nothing)
