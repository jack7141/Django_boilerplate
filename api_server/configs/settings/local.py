debug = True
from .base import get_secret, BASE_DIR

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
SECRET = get_secret(BASE_DIR)
SECRET_KEY = SECRET["SECRET_KEY"]

NEOMODEL_SIGNALS = True
NEOMODEL_FORCE_TIMEZONE = False
NEOMODEL_MAX_CONNECTION_POOL_SIZE = 50

DATABASES = SECRET["DATABASES"]

# Celery Configuration Options
for k, v in SECRET["CELERY"].items():
    locals()[f"CELERY_{k}"] = v

# django cache setting.
CACHES = SECRET["CACHES"]