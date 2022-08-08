#from django.shortcuts import render

#from django.http import HttpResponse

#from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from .serializers import NoteSerializer
from .models import Partner, User, Inventory, Product
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from .permissions import IsOwnerOrReadOnly
from .serializers import InventorySerializer, ProductSerializer, PartnerSerializer, RegisterSerializer
from .pagination import CustomPagination
from .filters import InventoryFilter
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


class UpdateUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    serializer_class = RegisterSerializer


class ListCreateInventoryAPIView(ListCreateAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = InventoryFilter

    def perform_create(self, serializer):
        # Assign the user who created the inventory
        serializer.save(partner=self.request.user)


class RetrieveUpdateDestroyInventoryAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListPartnerAPIView(ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class RetrieveUpdateDestroyPartnerAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ListCreateProductAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)


class RetrieveUpdateDestroyProductAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.username = data['email']
            # provider random default password
            user.password = make_password(BaseUserManager().make_random_password())
            user.email = data['email']
            user.save()

        token = RefreshToken.for_user(user)  # generate token without username & password
        response = {}
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response)






