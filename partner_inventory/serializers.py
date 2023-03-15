from rest_framework import serializers
from .models import Partner, User
from .models import Inventory, Product
from product_search.models import Customer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from datetime import datetime


class PartnerSerializer(serializers.ModelSerializer):  # create class to serializer model

    class Meta:
        model = Partner
        fields = ('shop_name', 'category',
                  'address_line_1', 'address_line_2', 'city_town', 'province_region_state', 'zip_code')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    partner = PartnerSerializer()

    class Meta:
        model = User
        fields = ('uuid', 'first_name', 'last_name', 'username', 'email', 'dob', 'is_email_verified', 'partner')

    def update(self, instance, validated_data):
        partner_serializer = self.fields['partner']
        partner_instance = instance.partner
        partner_data = validated_data.pop('partner', {})

        # to access the partner fields in here
        # mobile = partner_data.get('mobile')

        # update the partner fields
        partner_serializer.update(partner_instance, partner_data)

        instance = super().update(instance, validated_data)
        return instance


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
        fields = ('id', 'product_id', 'partner_id', 'partner', 'available', 'selling_price', 'product', 'image_url')
