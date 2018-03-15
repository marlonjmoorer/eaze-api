from rest_framework import serializers
from models import  Post, Comment, Profile,SocialLink
from users.serializers import UserSerializer



class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ("id",'link_type', 'url')



class ProfileSerializer(serializers.ModelSerializer):
    user=serializers.SlugRelatedField(slug_field='full_name',read_only=True)
    links=SocialLinkSerializer(many=True)
    posts=serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Profile
        fields = ('about','website','joined','photo','handle',"user","links","posts")
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
    tags= serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posted=serializers.DateField(required=False)
    author=ProfileSerializer(read_only=True)
    comments = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title','body',"posted","tags",'author','image','comments','slug','draft')


