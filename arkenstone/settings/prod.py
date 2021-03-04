import dj_database_url

from .base import *  # noqa

DENUG = False

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')  # noqa
    )
}
