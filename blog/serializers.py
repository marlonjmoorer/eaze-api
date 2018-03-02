from rest_framework import serializers
from models import  Post
class PostSerializer(serializers.ModelSerializer):

    title=serializers.CharField(required=True)
    body= serializers.CharField(required=True)
    tags= serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posted=serializers.DateField(required=False)
    author=serializers.SlugRelatedField(slug_field='full_name',read_only=True)
    #imageUrl= serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'title','body',"posted","tags",'author','image')


    def create(self, validated_data):
        return Post.objects.create(**validated_data)

