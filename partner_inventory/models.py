from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=5000)
    category = models.CharField(max_length=20)
    mrp = models.IntegerField()

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': ("A user with that username already exists."),
        },
    )
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
    dob = models.DateField(null=True)
    is_partner = models.BooleanField('partner status', default=False)
    is_customer = models.BooleanField('customer status', default=False)
    is_email_verified = models.BooleanField('email verification status', default=False)

    objects=UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Partner(models.Model):
    partner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    shop_name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)
    address_line_1 = models.TextField(max_length=150)
    address_line_2 = models.TextField(max_length=150)
    address_line_3 = models.TextField(max_length=150)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.partner


class Inventory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
    available = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.available
