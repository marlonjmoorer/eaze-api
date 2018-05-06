import json

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler

def eaze_exception_handler(exc, context):
    response = exception_handler(exc, context)
    try:
        detail = response.data['detail']
    except :
        detail = exc.message or exc
    response = HttpResponse(
        json.dumps({'detail': detail}),
        content_type="application/json", status=500
    )
    return response