from typing import Tuple

from django.db import transaction
from django.core.management.utils import get_random_secret_key

from utils import get_now

from users.models import User
from partner_inventory.models import Partner
from product_search.models import Customer


def user_create(email, is_partner=False, is_customer=False, password=None, **extra_fields) -> User:
    extra_fields = {
        **extra_fields
    }
    user = User(email=email, is_partner=is_partner, is_customer=is_customer, **extra_fields)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    if is_partner:
        Partner(partner_id=user.id).save()

    if is_customer:
        Customer(customer_id=user.id).save()

    return user


def user_record_login(*, user: User) -> User:
    user.last_login = get_now()
    user.save()

    return user


@transaction.atomic
def user_change_secret_key(*, user: User) -> User:
    user.secret_key = get_random_secret_key()
    user.full_clean()
    user.save()

    return user


@transaction.atomic
def user_get_or_create(*, email: str, **extra_data) -> Tuple[User, bool]:
    user = User.objects.filter(email=email).first()

    if user:
        return user, False

    return user_create(email=email, **extra_data), True
