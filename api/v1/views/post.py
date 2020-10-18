#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Posts

    Error codes:
        0: unknown error
        9: invalid path
        8: invalid parameter
        7: invalid request
"""

from models.post import Post
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from uuid import UUID


@app_views.route('/post', methods=['GET'], strict_slashes=False)
def get_posts():
    """
    Retrieves the list of all user objects
    or a specific user
    Return:
        {
            'error': "you must select a post but post id"
            'usage': "/post/post_id"
            'error_code': "9"
        }
    """
    response_dict = {}
    response_dict["error"] = "you must select a post but post id"
    response_dict["usage"] = "/post/<post_id>"
    response_dict["error_code"] = "9"
    return make_response(jsonify(response_dict), 202)


@app_views.route('/post/<post_id>', methods=['GET'], strict_slashes=False)
def get_post_byid(post_id):
    """
    Get Post information by post_id
    Return:
        if not valid user_id or no user found:
            error code: 8
        if success:
            return post info
        else
            unknown error (code : 0)
    """
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/post/<post_id>"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(post_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    post = storage.get(Post, post_id)
    if not post:
        return make_response(jsonify(response_dict), 202)
    else:
        post_info = post.to_dict()
        user_id = post_info["user_id"]
        user_info = storage.get(User, user_id)
        post_info["user_avatar"] = user_info.user_avatar
        post_info["full_name"] = user_info.full_name
        return make_response(jsonify(post_info), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/post/<post_id>', methods=['DELETE'], strict_slashes=False)
def delete_post(post_id):
    """
    delete post by post_id
    Return:
        if not valid user_id or no user found:
            error code: 8
        if success:
            return success code 200
        else
            unknown error (code : 0)
    """
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/post/<post_id>"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(post_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    post = storage.get(Post, post_id)
    if not post:
        return make_response(jsonify(response_dict), 202)
    else:
        storage.delete(post)
        storage.save()
        return make_response(jsonify({}), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/post/<user_id>/new', methods=['POST'], strict_slashes=False)
def make_new_post(user_id):
    """
    make a new post
    Return:
        if not valid user_id or no user found:
            error code: 8
        if success:
            return success code 200
        else
            unknown error (code : 0)
    """

    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/post/<user_id>/new"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(user_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify(response_dict), 202)
    else:
        if not request.get_json():
            invalid_dict = {}
            invalid_dict["error"] = "invalid request"
            invalid_dict["usage"] = "/post/<user_id>/new"
            invalid_dict["required_methods"] = "POST"
            invalid_dict["error_code"] = "7"
            return make_response(jsonify(response_dict), 202)
        else:
            data = request.get_json()
            #########
            #
            #
            #       setting up data from front to db will be here
            #
            #
            #########
            instance.save()
            return make_response(jsonify(instance.to_dict()), 201)
