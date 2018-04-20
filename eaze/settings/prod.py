from .base import  *

import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
DEBUG=True
ALLOWED_HOSTS = ['eaze-app-api.herokuapp.com']
SECRET_KEY= os.environ["SECRET"]
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

MEDIA_URL=os.environ['MEDIA_URL']