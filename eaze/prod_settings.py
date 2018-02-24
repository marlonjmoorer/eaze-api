from settings import  *


DATABASES={
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['NAME'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'HOST':os.environ['HOST'],
        'PORT':os.environ['PORT'],
    }
}