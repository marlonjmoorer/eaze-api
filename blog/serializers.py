from rest_framework import serializers
from models import  Post
class PostSerializer(serializers.ModelSerializer):

    title=serializers.CharField(required=True)
    body= serializers.CharField(required=True)
    tags= serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posted=serializers.DateField(required=False)
    author=serializers.SlugRelatedField(slug_field='full_name',read_only=True)
    imageUrl= serializers.CharField(required=False)

    class Meta:
        model = Post
        fields = ('id', 'title','body',"posted","tags",'author','imageUrl')


    def create(self, validated_data):
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(Post, self).update(instance, validated_data)