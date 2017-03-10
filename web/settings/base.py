# encoding: utf-8

import os

# TODO: change confidentials to environment variables

DEBUG = True
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_PASSWORD = os.environ.get('MONGO_PWD')
MONGO_PORT = os.environ.get('MONGO_PORT')
