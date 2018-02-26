from base import  *

import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
DEBUG=False
ALLOWED_HOSTS = ['eaze-app-api.herokuapp.com']
SECRET_KEY= os.environ["SECRET"]
# DATABASES={
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': os.environ['NAME'],
#         'USER': os.environ['USER'],
#         'PASSWORD': os.environ['PASSWORD'],
#         'HOST':os.environ['HOST'],
#         'PORT':os.environ['PORT'],
#     }
# }