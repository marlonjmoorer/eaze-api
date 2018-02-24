# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from users.serializers import  UserSerializer
from users.models import User
from rest_framework.response import Response
from rest_framework import status,viewsets
from rest_framework import generics
from rest_framework.permissions import AllowAny,BasePermission


class IsCreationOrIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated():
            if view.action == 'create':
                return True
            else:
                return False
        else:
            return True


class UseViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsCreationOrIsAuthenticated,)


