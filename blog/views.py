# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView,GenericAPIView
from rest_framework.parsers import FileUploadParser,JSONParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from eaze.permissions import IsListOrIsAuthenticated
from models import  Post,Comment
from serializers import  PostSerializer, CommentSerializer
from rest_framework.permissions import AllowAny,BasePermission,SAFE_METHODS





class PostList(ListCreateAPIView):
    queryset = Post.objects.filter(draft=False)
    serializer_class = PostSerializer
    permission_classes = (IsListOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser,)

    # def get(self, request, *args, **kwargs):
    #     post = Post.objects.all()
    #     serializer = PostSerializer(post,many=True)
    #     return Response(serializer.data)

    def perform_create(self, serializer):
        slug=slugify(self.request.data['title'])
        return serializer.save(author=self.request.user,slug=slug ,**self.kwargs)


class PostDetail(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



    def update(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset,slug=kwargs['slug'])
        serializer= self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    


    def retrieve(self, request, *args,**kwargs):
        instance= get_object_or_404(self.queryset, slug=kwargs['slug'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsListOrIsAuthenticated,)

    def perform_create(self, serializer):
        post=Post.objects.get(slug=self.request.data['slug'])
        return serializer.save(user=self.request.user,post=post, **self.kwargs)
