import os

DEBUG = True

TOKEN_SECRET = os.environ.get('SECRET_KEY') or 'JWT Token Secret String'

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///app.db'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

