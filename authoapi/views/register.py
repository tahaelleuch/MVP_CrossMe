#!/usr/bin/python3
"""user register"""
from flask import Flask, jsonify, request, make_response
from authoapi.views import app_views
from models.user import User
from flask import abort
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)


@app_views.route('/new_user/', methods=['POST'])
def create_users():
    """create  new users"""
    e = 'email'
    p = 'password'
    f = 'full_name'
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if e not in request.get_json():
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if p not in request.get_json():
        return make_response(jsonify({'error': 'Missing password'}), 400)
    if f not in request.get_json():
        return make_response(jsonify({'error': 'Missing Full name'}), 400)

    all_cls = storage.all(User)
    for value in all_cls.values():
        if value.email == request.get_json()[e]:
            return make_response(jsonify({'error': 'email already registred'}), 400)
    req_data = request.get_json()
    new= User()
    for k , v in req_data.items():
        setattr(new, k, v)
    new.save()
    return make_response(jsonify(new.as_dict_nopwd()), 201)
