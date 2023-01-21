from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.contrib.auth.models import UnicodeUsernameValidator
from django.contrib.auth.models import UserManager
from django.core.management.utils import get_random_secret_key

class User(AbstractBaseUser):
    #user_id = models.IntegerField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    secret_key = models.CharField(max_length=255, default=get_random_secret_key)
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
