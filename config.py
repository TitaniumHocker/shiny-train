# -*- coding: utf-8 -*-
from flask_babelex import Locale
from os import environ, path
import tempfile
from dotenv import load_dotenv
load_dotenv()


class BasicConfig():
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = environ.get('SECRET_KEY')
    API_KEY = environ.get('API_KEY')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = environ.get('SECURITY_PASSWORD_HASH')
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    BABEL_DEFAULT_LOCALE = 'ru'
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = True
    SECURITY_CONFIRMABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_EMAIL_SUBJECT_REGISTER = 'Добро пожаловать!'
    SECURITY_EMAIL_SUBJECT_CONFIRM = 'Подтверждение'
    SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE = 'Пароль был изменен'
    SECURITY_EMAIL_SUBJECT_PASSWORD_RESET = 'Запрос сброса пароля'
    SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE = 'Пароль был сброшен'


class DevelopmentConfig(BasicConfig):
    SECURITY_EMAIL_SENDER = environ.get('MAIL_USERNAME')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{path.join(path.dirname(__file__), "db.sqlite3")}'
    SECURITY_SEND_REGISTER_EMAIL = True
    DEBUG=True


class ProductionConfig(BasicConfig):
    SQLALCHEMY_DATABASE_URI = environ.get('DB_URI')
    SECURITY_EMAIL_SENDER = 'noreply@dev.titaniumhocker.ru'


class TestingConfig(DevelopmentConfig):
    SECURITY_EMAIL_SENDER = 'noreply-test@localhost'
    TESTING = True


configurations = {
    'prod': ProductionConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig
}
