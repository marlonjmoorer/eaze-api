# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.generics import ListCreateAPIView,RetrieveAPIView
from rest_framework.parsers import FileUploadParser,JSONParser,MultiPartParser
from rest_framework.response import Response

from eaze.permissions import IsListOrIsAuthenticated
from models import  Post,Comment
from serializers import  PostSerializer, CommentSerializer
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
        return serializer.save(author=self.request.user, **self.kwargs)


class PostDetail(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


    # def retrieve(self, request, *args,**kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsListOrIsAuthenticated,)

    def perform_create(self, serializer):

        return serializer.save(user=self.request.user, **self.kwargs)
