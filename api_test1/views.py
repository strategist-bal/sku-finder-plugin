from django.shortcuts import render

from django.http import HttpResponse

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import NoteSerializer
from .models import


# Create your views here.
