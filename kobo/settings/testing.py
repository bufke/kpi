# coding: utf-8
from mongomock import MongoClient as MockMongoClient

from .base import *

# For tests, don't use KoBoCAT's DB
DATABASES = {
    'default': env.db_url(
        'KPI_DATABASE_URL' if 'KPI_DATABASE_URL' in os.environ else 'DATABASE_URL',
        default='sqlite:///%s/db.sqlite3' % BASE_DIR
    ),
}

DATABASE_ROUTERS = ['kpi.db_routers.TestingDatabaseRouter']

TESTING = True

# Decrease prod value to speed-up tests
SUBMISSION_LIST_LIMIT = 100

ENV = 'testing'

# Run all Celery tasks synchronously during testing
CELERY_TASK_ALWAYS_EAGER = True


MONGO_CONNECTION_URL = 'mongodb://fakehost/formhub_test'
MONGO_CONNECTION = MockMongoClient(
    MONGO_CONNECTION_URL, j=True, tz_aware=True)
MONGO_DB = MONGO_CONNECTION['formhub_test']

ENKETO_URL = 'http://enketo.mock'
ENKETO_INTERNAL_URL = 'http://enketo.mock'
