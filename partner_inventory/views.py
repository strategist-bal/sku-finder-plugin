#from django.shortcuts import render

#from django.http import HttpResponse

#from django.shortcuts import render
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .serializers import NoteSerializer
from .models import Partner, User, Inventory, Product
from product_search.models import Customer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrReadOnly
from .serializers import InventorySerializer, ProductSerializer, PartnerSerializer, RegisterSerializer, UserSerializer
from .pagination import CustomPagination
from .filters import InventoryFilter, ProductFilter
from rest_framework.utils import json
import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UpdatePartnerView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'uuid'
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


class ListCreateInventoryAPIView(ListCreateAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InventoryFilter

    def post(self, request):
        inventory = Inventory.objects.create(product_id=request.data.get("product_id"), partner_id=self.request.user.id, available = request.data.get("available"))
        inventory.save()

        response = {}
        response['product_id'] = inventory.product_id
        response['available'] = inventory.available
        return Response(response)

    def get_queryset(self):
        return Inventory.objects.filter(partner_id=self.request.user.id)


class RetrieveUpdateDestroyInventoryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListCreateProductAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def post(self, request):
        product = Product()
        product.name = request.data.get("name")
        product.description = request.data.get("description")
        product.category = request.data.get("category")
        product.mrp = request.data.get("mrp")
        product.partner_id = self.request.user.id
        product.save()
        inventory = Inventory.objects.create(product_id=product.id, available=0, partner_id = self.request.user.id)
        inventory.save()

        response = {}
        response['name'] = product.name
        response['description'] = product.description
        response['category'] = product.category
        response['mrp'] = product.mrp
        return Response(response)


class RetrieveUpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


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
            if user.is_partner:
                user.is_partner = 1
                user.save()
                partner = Partner.objects.create(partner_id=user.id)
                partner.save()
        except User.DoesNotExist:
            user = User()
            user.last_login = datetime.datetime.now()
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            user.username = data['email']
            user.is_partner = 1
            user.is_customer = 1
            user.is_email_verified = True
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()
            partner = Partner.objects.create(partner_id=user.id)
            partner.save()
            customer = Customer.objects.create(customer_id=user.id)
            customer.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['uuid'] = user.uuid
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)






