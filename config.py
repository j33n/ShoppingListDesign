"""All configurations for different environments"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Global configurations"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '&\xb2\xc8\x80^H\xef\xb7\xc9\xb11\\\xf0\xe5}\xdd\xb8[O\x0b\tK\x0e\xbe'

class ProductionConfig(Config):
    """Production configurations"""
    DEBUG = False

class DevelopmentConfig(Config):
    """Development configurations"""
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    """Testing configurations"""
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True
