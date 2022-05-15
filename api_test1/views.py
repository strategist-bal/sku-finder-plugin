from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import Partner


# Create your views here.

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer


class RegisterView(generics.CreateAPIView):
    queryset = Partner.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
