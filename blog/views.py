# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import uuid
from django.conf import settings

from django.shortcuts import render
from django.core.files.storage import default_storage
# Create your views here.
from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.parsers import FileUploadParser,JSONParser,MultiPartParser
from rest_framework.response import Response

from eaze.permissions import IsListOrIsAuthenticated
from models import  Post
from serializers import  PostSerializer
from rest_framework.permissions import AllowAny,BasePermission,SAFE_METHODS





class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsListOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser,)
    def get(self, request, *args, **kwargs):
        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # if 'imageUrl' in self.request.data :
        #     url =  self.request.data["imageUrl"]
        #
        # elif 'imageFile' in self.request.FILES:
        #     file=self.request.FILES["imageFile"]
        #
        #     path=default_storage.save("%s/%s" % (uuid.uuid4(),file.name),file)
        #     url= os.path.join(settings.MEDIA_URL,path)

        return  serializer.save(author=self.request.user,**self.kwargs)

class PostDetail(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    # def retrieve(self, request, *args,**kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
