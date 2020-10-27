#!/usr/bin/python3
"""
api that handle all default RestFul API actions for Follow

    Error codes:
        0: unknown error
        9: invalid path
        8: invalid parameter
        6: operation already exist
        1: Unauthorized request
"""

from models.follow import Follow
from models.user import User
from api.v1.views import app_views
from flask import Flask, make_response, request, jsonify, redirect
from uuid import UUID
from datetime import datetime
from models import storage
from models.notification import Notification

my_secret = "onetwo"


@app_views.route('/new_follow/<follower_id>/<followed_id>/<the_secret>', methods=['POST'], strict_slashes=False)
def make_new_follow(follower_id, followed_id, the_secret):
    """
    Make a new follower
    Return:
        if not valid user_id or no user found:
            error code: 8
        if already exist:
            error code: 6
        if success:
            return success code 200
        else
            unknown error (code : 0)
    """
    if request.method == 'POST':

        if the_secret != my_secret:
            unauto_dict = {}
            unauto_dict["error"] = "unauthorised request"
            unauto_dict["error_code"] = "1"
            return make_response(jsonify(unauto_dict), 401)

        response_dict = {}
        response_dict["error"] = "invalid parameter"
        response_dict["usage"] = "new_follow/<follower_id>/<followed_id>"
        response_dict["error_code"] = "8"

        try:
            uuid_obj = UUID(follower_id, version=4)
            uuid_obj = UUID(followed_id, version=4)
        except ValueError:
            return make_response(jsonify(response_dict), 202)

        user_1 = storage.get(User, follower_id)
        user_2 = storage.get(User, followed_id)
        if not user_1 or not user_2:
            return make_response(jsonify(response_dict), 202)


        if storage.get_by_two(Follow, follower_id, followed_id) is not None:
            al_exist = {}
            al_exist["error"] = "operation already exist"
            al_exist["usage"] = "new_follow/<follower_id>/<followed_id>"
            al_exist["error_code"] = "6"
            return make_response(jsonify(al_exist), 202)


        new_follow = Follow()
        new_follow.follower_id = follower_id
        new_follow.user_id = followed_id
        new_follow.follow_code = 1
        new_follow.creation_date = datetime.utcnow()
        new_follow.save()

        new_notif = Notification()
        new_notif.reciver_user_id = followed_id
        new_notif.maker_user_id = follower_id
        new_notif.type = "follow"
        new_notif.follow_id = str(new_follow.id)
        new_notif.creation_date = datetime.utcnow()
        new_notif.save()

        succ = {}
        succ["status"] = "ok"
        return make_response(jsonify(succ), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/del_follow/<follower_id>/<followed_id>/<the_secret>', methods=['DELETE'], strict_slashes=False)
def delete_follow(follower_id, followed_id, the_secret):
    """
    Make a new follower
    Return:
        if not valid user_id or no user found:
            error code: 8
        if success:
            return success code 200
        else
            unknown error (code : 0)
    """
    if request.method == 'DELETE':

        if the_secret != my_secret:
            unauto_dict = {}
            unauto_dict["error"] = "unauthorised request"
            unauto_dict["error_code"] = "1"
            return make_response(jsonify(unauto_dict), 401)

        response_dict = {}
        response_dict["error"] = "invalid parameter"
        response_dict["usage"] = "/del_follow/<follower_id>/<followed_id>"
        response_dict["error_code"] = "8"

        try:
            uuid_obj = UUID(follower_id, version=4)
            uuid_obj = UUID(followed_id, version=4)
        except ValueError:
            return make_response(jsonify(response_dict), 202)

        user_1 = storage.get(User, follower_id)
        user_2 = storage.get(User, followed_id)
        if not user_1 or not user_2:
            return make_response(jsonify(response_dict), 202)

        the_obj = storage.get_by_two(Follow, follower_id, followed_id)

        print (the_obj)
        print (the_obj.to_dict())
        if not the_obj:
            return make_response(jsonify(response_dict), 202)
        else:
            the_obj.delete()
            storage.save()
            storage.reload()
            return make_response(jsonify({}), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/follow_code/<follower_id>/<followed_id>', methods=['GET'], strict_slashes=False)
def get_status_code(follower_id, followed_id):
    """
    Make a new follower
    Return:
         if not valid user_id or no user found:
             error code: 8
         if success:
             return success code 200
         else
             unknown error (code : 0)
    """
    if request.method == 'POST':
        response_dict = {}
        response_dict["error"] = "invalid parameter"
        response_dict["usage"] = "/del_follow/<follower_id>/<followed_id>"
        response_dict["error_code"] = "8"

        try:
            uuid_obj = UUID(follower_id, version=4)
            uuid_obj = UUID(followed_id, version=4)
        except ValueError:
            return make_response(jsonify(response_dict), 202)

        user_1 = storage.get(User, follower_id)
        user_2 = storage.get(User, followed_id)
        if not user_1 or not user_2:
            return make_response(jsonify(response_dict), 202)

        the_obj = storage.get_by_two(Follow, follower_id, followed_id)

        if not the_obj:
            return make_response(jsonify(response_dict), 202)
        else:
            follow_obj = storage.get_by_two(Follow, follower_id, followed_id)
            obj_code = follow_obj.follow_code
            resp_dict = {}
            resp_dict["code"] = obj_code
            return make_response(jsonify(resp_dict), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)
