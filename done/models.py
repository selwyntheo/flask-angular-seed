from datetime import datetime, timedelta
import os
import jwt
import json
import requests
import base64
from functools import wraps
from urlparse import parse_qs, parse_qsl
from urllib import urlencode
from flask import Flask, g, send_file, request, redirect, url_for, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_user import roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from requests_oauthlib import OAuth1
from jwt import DecodeError, ExpiredSignature

from .done import db

from .utils import timestamp, url_for

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    display_name = db.Column(db.String(120))
    facebook = db.Column(db.String(120))
    github = db.Column(db.String(120))
    google = db.Column(db.String(120))
    linkedin = db.Column(db.String(120))
    twitter = db.Column(db.String(120))
    bitbucket = db.Column(db.String(120))

    def __init__(self, email=None, password=None,  display_name=None,
                 facebook=None, github=None, google=None, linkedin=None,
                 twitter=None, bitbucket=None):
        if email:
            self.email = email.lower()
        if password:
            self.set_password(password)
        if display_name:
            self.display_name = display_name
        if facebook:
            self.facebook = facebook
        if google:
            self.google = google
        if linkedin:
            self.linkedin = linkedin
        if twitter:
            self.twitter = twitter
        if bitbucket:
            self.bitbucket = bitbucket
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def export_data(self):
        return {
            'name': self.display_name
        }

    def to_json(self):
        return dict(id=self.id, email=self.email, displayName=self.display_name,
                    facebook=self.facebook, google=self.google,
                    linkedin=self.linkedin, twitter=self.twitter,
                    bitbucket=self.bitbucket)

