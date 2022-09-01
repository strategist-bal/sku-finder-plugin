#from django.shortcuts import render

#from django.http import HttpResponse

#from django.shortcuts import render
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .serializers import NoteSerializer
from .models import Customer, Address
from partner_inventory.models import User, Product
from product_search.models import Customer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from rest_framework.utils import json
import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from partner_inventory.serializers import ProductSerializer
from partner_inventory.pagination import CustomPagination


class ListProductAPIView(ListAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v1/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.last_login = datetime.datetime.now()
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            user.username = data['email']
            user.is_partner = 0
            user.is_customer = 1
            user.is_email_verified = True
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            customer = Customer.objects.create(partner_id=user.id)
            customer.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['uuid'] = user.uuid
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)