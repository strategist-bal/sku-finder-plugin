import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Partner, Inventory, Product
from users.models import User
from product_search.models import Customer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrReadOnly, IsOwner
from .serializers import InventorySerializer, ProductSerializer, PartnerSerializer, UserSerializer
from .pagination import CustomPagination
from .filters import InventoryFilter, ProductFilter
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
from api.product_image import generate_presigned_url
import boto3
import uuid


class ListPartnerView(ApiAuthMixin, ApiErrorsMixin, ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UpdatePartnerView(ApiAuthMixin, ApiErrorsMixin, RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'uuid'
    #permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


class ListCreateInventoryAPIView(ApiAuthMixin, ApiErrorsMixin, ListCreateAPIView):
    serializer_class = InventorySerializer
    #permission_classes = [IsAuthenticated]
    #filter_backends = (filters.DjangoFilterBackend,)
    #filterset_class = InventoryFilter
    pagination_class = CustomPagination
    # filterset_fields  = ['product','product__name']

    def post(self, request):
        inventory = Inventory.objects.create(product_id=request.data.get("product_id"), partner_id=self.request.user.id,
                                             available = request.data.get("available"), selling_price=request.data.get("selling_price"),
                                             image_url=request.data.get("image_url"))
        inventory.save()

        response = {}
        response['product_id'] = inventory.product_id
        response['available'] = inventory.available
        response['selling_price'] = inventory.selling_price
        return Response(response)

    def get_queryset(self):
        queryset = Inventory.objects.filter(partner_id=self.request.user.id)
        product_name = self.request.query_params.get('name')
        category = self.request.query_params.get('category')

        if product_name:
            queryset = queryset.filter(product__name__icontains=product_name)
        elif category:
            queryset = queryset.filter(product__category=category)

        return queryset


class GetPresignedImageUrl(ApiAuthMixin, ApiErrorsMixin, CreateAPIView):

    def post(self, request):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.ACCESS_KEY,
            aws_secret_access_key=settings.SECRET_KEY,
            region='ap-south-1'
        )
        client_action = 'get_object' if request.data.get("action") == 'get' else 'put_object'
        key = str(self.request.user.uuid) + "/" + str(uuid.uuid4()) + "." + request.data.get("type").split("/")[1]
        url = generate_presigned_url(
            s3_client, client_action, {'Bucket': settings.BUCKET, 'Key': key,'ACL':"public-read"}, 9000)

        response = {}
        response['key'] = key
        response['presigned_imageurl'] = url
        response['access_url'] = "https://s3.ap-south-1.amazonaws.com/"+settings.BUCKET+"/"+key
        return Response(response)


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

        response = {}
        response['product_id'] = product.id
        response['name'] = product.name
        response['description'] = product.description
        response['category'] = product.category
        response['mrp'] = product.mrp
        return Response(response)


class RetrieveUpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()





