from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.utils.datetime_safe import datetime
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

from users.serializers import UserSerializer


class ObtainUserAuthToken(ObtainJSONWebToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = {
                'token': token,
                'user': UserSerializer(user).data
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            return response

        return super(ObtainUserAuthToken,self).post(request, *args, **kwargs)