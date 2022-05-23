from rest_framework import serializers
from .models import Partner
from .models import Inventory, Product
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Partner.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = Partner
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'dob')

    def create(self, validated_data):
        partner = Partner.objects.create(**validated_data)

        partner.set_password(validated_data['password'])
        partner.save()

        return partner


class InventorySerializer(serializers.ModelSerializer):  # create class to serializer model
    partner = serializers.ReadOnlyField(source='partner.id')

    class Meta:
        model = Inventory
        fields = ('id', 'product', 'partner', 'available')


class ProductSerializer(serializers.ModelSerializer):  # create class to serializer model
    #partner = serializers.ReadOnlyField(source='partner.username')

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'category', 'mrp')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    inventory = serializers.PrimaryKeyRelatedField(many=True, queryset=Inventory.objects.all())

    class Meta:
        model = Partner
        fields = ('id', 'username', 'inventory')
