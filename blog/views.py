from django.http import Http404
from django.template.defaultfilters import slugify
from rest_framework import filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.viewsets import ModelViewSet
from blog.models import *
from blog.serializers import *
from eaze.permissions import IsCreationOrIsAuthenticated,IsGetOrIsAuthenticated
from rest_framework.decorators import list_route,detail_route
from django.shortcuts import get_object_or_404,get_list_or_404
from django_filters.rest_framework import  DjangoFilterBackend
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'
    filter_fields = ('draft',)
    filter_backends = (filters.SearchFilter,DjangoFilterBackend,)
    search_fields = ('slug', 'tags__slug', 'title', 'author__handle')

    def create(self, request, *args, **kwargs):
        slug = slugify(self.request.data['title'])
        author = Profile.objects.get(user=self.request.user)
        data = self.request.data.copy()
        tags = []
        if "tags" in data:
             tags = json.loads(data["tags"])
             data['tags']=tags
        post=PostSerializer(data=data)
        post.is_valid(raise_exception=True)
        post.save(author=author,tags=tags, slug=slug, **self.kwargs)
        return Response(post.data)

    @detail_route(methods=["get"])
    def comments(self,request,pk=None):
        commnets=Comment.objects.filter(post=pk)
        serializer =CommentSerializer(commnets,many=True)
        return Response(serializer.data)

class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
   # permission_classes = (IsGetOrIsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug',)


class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'handle'

    def patch(self, request, *args, **kwargs):
        if request.user:
            links = []
            if "links" in request.data:
                links = json.loads(request.data["links"])
                linkSet = SocialLinkSerializer(data=links, many=True)
                linkSet.is_valid(raise_exception=True)
            instance = get_object_or_404(self.queryset, user=request.user)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(links=links)

            return Response(serializer.data)

        raise PermissionDenied(detail="No User was found", code=401)

    @detail_route(methods=["post"])
    def follow(self, request, handle):
        if request.user:
            instance = get_object_or_404(self.queryset, user=request.user)
            id= get_object_or_404(self.queryset, handle=handle).pk
            if instance.following.filter(pk=id).exists():
                instance.following.remove(id)
            else:
                instance.following.add(id)
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        raise Http404



    @detail_route()
    def following(self,request,handle):
        profile_id = get_object_or_404(self.queryset, handle=handle).pk
        following=get_list_or_404(self.queryset,followers=profile_id)
        serializers=self.serializer_class(following,many=True)
        return  Response(serializers.data)

    @detail_route()
    def posts(self,request,handle):
        profile_id=get_object_or_404(self.queryset,handle=handle).pk
        posts= Post.objects.filter(author=profile_id)
        serializer =PostSerializer(posts,many=True)
        return  Response(serializer.data)
   # permission_classes = (IsGetOrIsAuthenticated,)

class CommentViewSet(ModelViewSet):
    queryset =  Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        data = self.request.data.copy()
        profile = Profile.objects.get(user=self.request.user)
        post= Post.objects.get(pk=data["post_id"])
        comment = CommentSerializer(data=data)
        comment.is_valid(raise_exception=True)
        comment.save(profile=profile,post=post, **self.kwargs)
        return Response(comment.data)


    @detail_route()
    def replies(self, request, pk):
        replies =Comment.objects.filter(parent=pk)
        serializer = CommentSerializer(replies, many=True)
        return Response(serializer.data)