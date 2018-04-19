from rest_framework import serializers
from models import Post, Comment, Profile, SocialLink, Tag
from users.serializers import UserSerializer



class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("id",'link_type', 'url')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields ='__all__'


class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.SlugRelatedField(slug_field='full_name',read_only=True)
    links=SocialLinkSerializer(many=True)
    posts=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    following=serializers.PrimaryKeyRelatedField(many=True,queryset=Profile.objects.all())
    followers=serializers.PrimaryKeyRelatedField(many=True,queryset=Profile.objects.all())
    class Meta:
        model = Profile
        fields = ("id",'about','website','joined','photo','handle',"user","links","posts","following","followers")
        depth = 2

    def update(self, instance, validated_data):
        instance.about=validated_data.get("about",instance.about)
        instance.website = validated_data.get("website", instance.website)

        photo = validated_data.get("photo",None)
        if photo and  not isinstance(photo, str):
             instance.photo=photo

        instance.save()
        links= validated_data.get("links")
        if links:
            for linkdata in links:
                if "id" in linkdata:
                    shouldDelete=linkdata.pop("delete", None)
                    link = SocialLink(**linkdata)
                    link.profile=instance
                    if shouldDelete:
                        link.delete()
                    else:
                        link.save()
                else:
                    SocialLink.objects.create(profile=instance,**linkdata)

        return instance

class CommentSerializer(serializers.ModelSerializer):
    user =  UserSerializer(read_only=True)
    class Meta:
        model=Comment
        fields=("user","body","created")
    def create(self, validated_data):
       comment=Comment.objects.create(**validated_data)
       return comment

class PostSerializer(serializers.ModelSerializer):

    title=serializers.CharField(required=True)
    body= serializers.CharField(required=True)
    tags=  TagSerializer(many=True) #serializers.PrimaryKeyRelatedField(many=True,queryset=Tag.objects.all())
    posted=serializers.DateField(required=False)
    author=ProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title','body',"posted","tags",'author','image','comments','slug','draft')

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)
        instance =Post(**validated_data)
        instance.save()
        if tags:
            tags =[Tag(**data).pk for data in tags]
            instance.tags.add(*tags)
        instance.save()
        return instance


    def update(self, instance, validated_data):

        tags = validated_data.pop("tags",None)
        instance.title= validated_data.get("title")
        instance.body= validated_data.get("body")

        if tags:
            tags =[Tag(**data).pk for data in tags]
            instance.tags.clear()
            instance.tags.add(*tags)

        instance.save()
        return instance

