from rest_framework import serializers
from .models import Partner
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
