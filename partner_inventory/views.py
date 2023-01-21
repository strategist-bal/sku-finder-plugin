import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Partner, Inventory, Product, Listing
from users.models import User
from product_search.models import Customer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrReadOnly
from .serializers import InventorySerializer, ProductSerializer, PartnerSerializer, RegisterSerializer, UserSerializer, \
    ListingSerializer
from .pagination import CustomPagination
from .filters import InventoryFilter, ProductFilter, ListingFilterSet
from rest_framework.utils import json
import requests
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, serializers
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.compat import set_cookie_with_token
from django.conf import settings
from django.shortcuts import redirect
from api.mixins import ApiErrorsMixin, ApiAuthMixin, PublicApiMixin
import os


class ListCreateListingView(ApiAuthMixin, ApiErrorsMixin, ListCreateAPIView):
    serializer_class = ListingSerializer
    queryset = Listing.objects.select_related('inventory').all()
    #permission_classes = [IsAuthenticated]
    filterset_class = ListingFilterSet

    def post(self, request):
        listing = Listing.objects.create(inventory_id=request.data.get("inventory_id"), partner_id=self.request.user.id , \
                                         selling_price=request.data.get("selling_price"))
        listing.save()

        response = {}
        response['inventory_id'] = listing.inventory_id
        response['selling_price'] = listing.selling_price
        return Response(response)

    def get_queryset(self):
        return Listing.objects.filter(partner_id=self.request.user.id)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UpdatePartnerView(ApiAuthMixin, ApiErrorsMixin, RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'uuid'
    #permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


class ListCreateInventoryAPIView(ApiAuthMixin, ApiErrorsMixin, ListCreateAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    #permission_classes = [IsAuthenticated]
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


class RetrieveUpdateDestroyInventoryAPIView(ApiAuthMixin, ApiErrorsMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    #permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListCreateProductAPIView(ApiAuthMixin, ApiErrorsMixin, ListCreateAPIView):
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
        print(self.request.user.is_authenticated)
        print(self.request.user.id)
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





