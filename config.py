# -*- encoding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@192.168.1.147:3306/flask?charset=utf8'
DEBUG = True

INSTALLED_APPS = [
    'account',
    'gitlab',
    'jenkins'
]
