from .base import  *

import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600)
DEBUG=True
ALLOWED_HOSTS = ['eaze-app-api.herokuapp.com']
SECRET_KEY= os.environ["SECRET"]
