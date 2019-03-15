class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = 'my precious'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mightmight@localhost/myflaskrest'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True # allows error from flask_jwt to be raised accordingly
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
