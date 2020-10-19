#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Users

    Error codes:
        0: unknown error
        9: invalid path
        8: invalid parameter
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from uuid import UUID


@app_views.route('/search/<pattern>', methods=['GET'], strict_slashes=False)
def searchbypattern(pattern):
    """
    Get user information by user_id
    Return:
        if not valid user_id or no user found:
            error code: 8
        if success:
            return user info
        else
            unknown error (code : 0)
    """
    if len(pattern)>25:
        return make_response(jsonify({'error': "Bad Request"}), 404)
    f = pattern.sp 
    for i in storage.all(User):
        print(i)
    return make_response(jsonify({'done': "200"}), 202)