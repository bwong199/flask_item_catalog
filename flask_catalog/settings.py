import os

SECRET_KEY = 'some-secret-key'
DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'root'
CATALOG_DATABASE_NAME = 'catalog'
DB_HOST = os.getenv('IP', '0.0.0.0')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, CATALOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLACLCHEMY_TRACK_MODIFICATIONS = True

