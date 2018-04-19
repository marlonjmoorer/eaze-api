import json

from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotFound
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken

from users.serializers import UserSerializer

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer


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

@csrf_exempt
@renderer_classes((JSONRenderer,))
def ObtainUser(request):
    data=json.loads(request.body)
    valid_data = VerifyJSONWebTokenSerializer().validate(data)
    user = valid_data['user']
    response_data = {
        'user': UserSerializer(user).data
    }
    return JsonResponse(response_data, status=status.HTTP_200_OK)