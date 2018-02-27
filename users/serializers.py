
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import  User


class UserSerializer(serializers.ModelSerializer):

    email= serializers.EmailField(required=True,validators=[UniqueValidator(
        queryset=User.objects.all(),
        message="Email is already in use"
    )])
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    password= serializers.CharField(write_only=True,min_length=8,
                                    error_messages={"min_length":"Password must be 8 characters"})


    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','password')


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

