
from rest_framework import serializers
from users.models import  User


class UserSerializer(serializers.ModelSerializer):

    username= serializers.CharField(required=True)
    email= serializers.EmailField(required=True)
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    password= serializers.CharField(write_only=True)


    class Meta:
        model = User
        fields = ('id', 'username','email','first_name','last_name','password')


    def create(self, validated_data):

        user=User.objects.create(**validated_data)
        password = validated_data.pop('password')
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

