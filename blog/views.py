# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import get_object_or_404,get_list_or_404
from django.template.defaultfilters import slugify
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView,GenericAPIView, ListAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import FileUploadParser,JSONParser,MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from eaze.permissions import IsGetOrIsAuthenticated
from models import Post, Comment, Profile, SocialLink
from serializers import  PostSerializer, CommentSerializer, ProfileSerializer

from users.models import User
import  json

#/post
class PostList(ListCreateAPIView):
    queryset = Post.objects.filter(draft=False)
    serializer_class = PostSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser,)
    def perform_create(self, serializer):
        slug=slugify(self.request.data['title'])
        author=Profile.objects.get(user=self.request.user)
        return serializer.save(author=author,slug=slug ,**self.kwargs)

class PostByAuthor(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        name = kwargs["name"]
        if(name):
            user=Profile.objects.get(handle=name)
            queryset=self.get_queryset()
            post= queryset.filter(author_id=user.pk)
            serializer=PostSerializer(post,many=True)

        return Response(serializer.data)

class PostDetail(RetrieveUpdateAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsGetOrIsAuthenticated,)

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


#/comments
class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsGetOrIsAuthenticated,)

    def perform_create(self, serializer):
        post=Post.objects.get(slug=self.request.data['slug'])
        return serializer.save(user=self.request.user,post=post, **self.kwargs)

#/profile
class ProfileDetail(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser)

    def patch(self, request, *args, **kwargs):
        if request.user:
            data=request.data.copy()
            links=[]
            if "links" in data:
                 links=json.loads(data["links"])
                 data["links"]=links
            instance = get_object_or_404(self.queryset, user=request.user)
            serializer = self.get_serializer(instance, data=data,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(links=links)

            return Response(serializer.data)

        return None


    def retrieve(self, request,*args,**kwargs):
        if "handle" in kwargs:
            instance= get_object_or_404(self.queryset,handle=kwargs['handle'])
        elif request.user:
            instance = get_object_or_404(self.queryset,user=request.user)
        else:
            raise Http404('No profile found')
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
