from rest_framework import serializers
from .models import Partner, User
from .models import Inventory, Product
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'dob', 'is_partner', 'is_customer')

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user


class InventorySerializer(serializers.ModelSerializer):  # create class to serializer model
    partner = serializers.ReadOnlyField(source='partner.id')

    class Meta:
        model = Inventory
        fields = ('id', 'product', 'partner', 'available')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    class Meta:
        model = User
        fields = ('id', 'uuid', 'first_name','last_name','username','email','dob','is_email_verified')


class PartnerSerializer(serializers.ModelSerializer):  # create class to serializer model
    partner = UserSerializer()
    class Meta:
        model = Partner
        fields = ('partner_id', 'partner', 'shop_name', 'category',
                 'address_line_1', 'address_line_2', 'address_line_3', 'latitude', 'longitude')


class ProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'mrp')



