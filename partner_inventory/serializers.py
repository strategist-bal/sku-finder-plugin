from rest_framework import serializers
from .models import Partner, User
from .models import Inventory, Product, Listing
from product_search.models import Customer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import datetime


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'dob', 'is_partner', 'is_customer', 'uuid')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.last_login = datetime.now()
        user.set_password(validated_data['password'])
        user.is_customer = 0
        user.is_partner = 1
        user.save()
        partner = Partner.objects.create(partner_id=user.id)
        partner.save()
        return user


class PartnerSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = Partner
        fields = ('shop_name', 'category',
                  'address_line_1', 'address_line_2', 'address_line_3', 'latitude', 'longitude')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    partner = PartnerSerializer()

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'username', 'email', 'dob', 'is_email_verified', 'partner')


class ProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    partner = serializers.ReadOnlyField(source='partner.id')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'mrp', 'partner')


class InventorySerializer(serializers.ModelSerializer):  # create class to serializer model
    partner = serializers.ReadOnlyField(source='partner.id')
    product = ProductSerializer()

    class Meta:
        model = Inventory
        fields = ('id', 'product_id', 'partner_id', 'partner', 'available', 'product')


class ListingSerializer(serializers.ModelSerializer):
    partner = serializers.ReadOnlyField(source='partner.id')
    inventory = InventorySerializer()

    class Meta:
        model = Listing
        fields = ('id', 'selling_price', 'partner_id', 'inventory', 'partner')
