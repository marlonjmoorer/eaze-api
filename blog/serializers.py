from rest_framework import serializers
from models import  Post, Comment
from users.serializers import UserSerializer



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
    author=serializers.SlugRelatedField(slug_field='full_name',read_only=True)
    comments = CommentSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title','body',"posted","tags",'author','image','comments','slug','draft')



