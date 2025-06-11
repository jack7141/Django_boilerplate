from .base import *

SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY')
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': env.get('DATABASE_NAME'),
        'USER': env.get('DATABASE_USER'),
        'PASSWORD': env.get('DATABASE_PASSWORD'),
        'HOST': env.get('DATABASE_HOST'),
        'PORT': env.get('DATABASE_PORT'),
        "CONN_MAX_AGE": 600
    }
}