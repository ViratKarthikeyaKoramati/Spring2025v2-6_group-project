import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'college_event_mgmt_secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///college_event_management.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Email Configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'youremail@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'yourpassword'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

# Mapping of configuration modes
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}