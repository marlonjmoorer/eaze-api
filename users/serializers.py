
from rest_framework import serializers
from users.models import  User


class UserSerializer(serializers.ModelSerializer):

    username= serializers.CharField(required=False)
    email= serializers.EmailField(required=False)


    class Meta:
        model = User
        fields = ('id', 'username','email')


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """

        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserSerializer, self).update(instance, validated_data)

