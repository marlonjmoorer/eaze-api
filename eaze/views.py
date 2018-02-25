from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.http import HttpResponseNotFound


def media(resquest,filename):
    if default_storage.exists(filename):
        file=default_storage.open(filename)
        fileData=file.read()
        return HttpResponse(fileData, content_type="image/png")
    return HttpResponseNotFound('<h1>Page not found</h1>')