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

# Configuration

current_path = os.path.dirname(__file__)
client_path = os.path.abspath(os.path.join(current_path,  'static'))

app = Flask(__name__, static_url_path='/static')
app.config.from_object('config')

db = SQLAlchemy(app)



from .models import *

def create_token(user):
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(days=14)
    }
    token = jwt.encode(payload, app.config['TOKEN_SECRET'])
    return token.decode('unicode_escape')


def parse_token(req):
    token = req.headers.get('Authorization').split()[1]
    return jwt.decode(token, app.config['TOKEN_SECRET'])


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function




# Routes
@app.route('/views/<path:filename>')
def getView(filename):
    return app.send_static_file('views/' + filename)

@app.route('/js/<path:filename>')
def getJsFile(filename):
    return app.send_static_file('js/' + filename)

@app.route('/fonts/<path:filename>')
def getFontsFile(filename):
    return app.send_static_file('fonts/' + filename)

@app.route('/css/<path:filename>')
def getCssFile(filename):
    return app.send_static_file('css/' + filename)

@app.route('/img/<path:filename>')
def getImgFile(filename):
    return app.send_static_file('img/' + filename)



@app.route('/')
def index():
    return send_file(os.path.join(client_path, 'index.html'))


@app.route('/api/me')
@login_required
def me():
    user = User.query.filter_by(id=g.user_id).first()
    return jsonify(user.to_json())


@app.route('/auth/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.json['email']).first()
    if not user or not user.check_password(request.json['password']):
        response = jsonify(message='Wrong Email or Password')
        response.status_code = 401
        return response
    token = create_token(user)
    return jsonify(token=token)


@app.route('/auth/signup', methods=['POST'])
def signup():
    user = User(email=request.json['email'], password=request.json['password'], display_name=request.json['displayName'])
    db.session.add(user)
    db.session.commit()
    token = create_token(user)
    return jsonify(token=token)