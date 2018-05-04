# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import Http404
from django.shortcuts import get_object_or_404,get_list_or_404
from django.template.defaultfilters import slugify
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateAPIView, ListAPIView,UpdateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, filters
from eaze.permissions import IsGetOrIsAuthenticated
from .models import Post, Comment, Profile, SocialLink, Tag
from .serializers import PostSerializer, CommentSerializer, ProfileSerializer, SocialLinkSerializer, TagSerializer


import  json

#/post
class PostList(ListCreateAPIView):
    queryset = Post.objects.filter(draft=False)
    serializer_class = PostSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('slug','tags__name','title','author__handle')



    def perform_create(self, serializer):
        slug=slugify(self.request.data['title'])
        author=Profile.objects.get(user=self.request.user)
        data = self.request.data.copy()
        tags=[]
        if "tags" in data:
            tags=TagList.extractTags(data)
        return serializer.save(author=author,tags=tags,slug=slug ,**self.kwargs)

class PostDetail(RetrieveUpdateDestroyAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser,)
    def update(self, request, *args, **kwargs):
        tags = []
        data=request.data.copy()
        if "tags" in data:
            tags=TagList.extractTags(data)
        instance = get_object_or_404(self.queryset, slug=kwargs['slug'])
        serializer= self.get_serializer(instance, data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(tags=tags)
        return Response(serializer.data)

    def retrieve(self, request, *args,**kwargs):
        instance= get_object_or_404(self.queryset, slug=kwargs['slug'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    def delete(self, request, *args, **kwargs):
        instance = get_object_or_404(self.queryset,author=request.user.profile,pk=kwargs["id"])
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








#/comments
class CommentList(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsGetOrIsAuthenticated,)

    def perform_create(self, serializer):
        parent=None
        post=Post.objects.get(slug=self.request.data['slug'])
        profile= Profile.objects.get(user=self.request.user)
        if("parent" in self.request.data):
            parent=get_object_or_404(self.queryset,id=self.request.data['parent'])
        return serializer.save(profile=profile,post=post, **self.kwargs)

class CommentListReplies(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsGetOrIsAuthenticated,)

    def list(self, request, *args, **kwargs):

        replies= get_list_or_404(self.queryset,parent=kwargs["id"])
        serializer = self.get_serializer(replies,many=True)
        return Response(serializer.data)

#/profile
class ProfileDetail(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    parser_classes = (JSONParser,MultiPartParser)

    def patch(self, request, *args, **kwargs):
        if request.user:
            links=[]
            if "links" in request.data:
                 links=json.loads(request.data["links"])
                 linkSet=SocialLinkSerializer(data=links,many=True)
                 linkSet.is_valid(raise_exception=True)
            instance = get_object_or_404(self.queryset, user=request.user)
            serializer = self.get_serializer(instance, data=request.data,partial=True)
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


class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsGetOrIsAuthenticated,)
    search_fields = ('handle',)


class PostByAuthor(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsGetOrIsAuthenticated,)
    def list(self, request, *args, **kwargs):
        name = kwargs["name"]
        if (name):
            user = Profile.objects.get(handle=name)
            queryset = self.get_queryset()
            post = queryset.filter(author_id=user.pk)
            serializer = PostSerializer(post, many=True)

        return Response(serializer.data)


class FollowAuthor(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def patch(self, request, *args, **kwargs):
        if request.user:
            add = request.data["add"]
            id = request.data["id"]
            instance = get_object_or_404(self.queryset, user=request.user)

            if not add and instance.following.filter(pk=id).exists():
                instance.following.remove(id)
            elif add:
                instance.following.add(id)
            else:
                raise Http404
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        raise Http404


#/tags
class TagList(ListAPIView):
        permission_classes = (IsGetOrIsAuthenticated,)
        queryset = Tag.objects.all()
        serializer_class = TagSerializer
        filter_backends = (filters.SearchFilter,)
        search_fields = ('name','slug',)

        @staticmethod
        def extractTags(data):
            tags = json.loads(data["tags"])
            TagSerializer(data=tags, many=True).is_valid(raise_exception=True)
            data.pop("tags")
            return tags



