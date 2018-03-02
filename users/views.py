# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from eaze.permissions import IsCreationOrIsAuthenticated
from users.serializers import  UserSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny,BasePermission




class UseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreationOrIsAuthenticated,)


