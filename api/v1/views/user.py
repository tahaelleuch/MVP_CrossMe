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



@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """
    Retrieves the list of all user objects
    or a specific user
    Return:
        {
            'error': "you must select a user but it id"
            'usage': "/users/user_id"
            'error_code': "9"
        }
    """
    response_dict = {}
    response_dict["error"] = "you must select a user but it id"
    response_dict["usage"] = "/users/<user_id>"
    response_dict["error_code"] = "9"
    return make_response(jsonify(response_dict), 202)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_byid(user_id):
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
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/users/<user_id>"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(user_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify(response_dict), 202)
    else:
        user_info = user.to_dict()
        return make_response(jsonify(user_info), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/users/email/<user_email>', methods=['GET'], strict_slashes=False)
def get_user_byemail(user_email):
    """
    Get user information by email
    Return:
        if not valid user_email or no user found:
            error code: 8
        if success:
            return user info
        else
            unknown error (code : 0)
    """
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/users/<user_id>"
    response_dict["error_code"] = "8"

    if user_email.find("@") == -1:
        return make_response(jsonify(response_dict), 202)
    else:
        user = storage.getbyemail(User, user_email)
        if not user:
            return make_response(jsonify(response_dict), 202)
        else:
            user_info = user.to_dict()
            return make_response(jsonify(user_info), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)

