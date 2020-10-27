#!/usr/bin/python3
""" API actions for Reactions """

from models.user import User
from models.notification import Notification
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from uuid import UUID


@app_views.route('/notif/<user_id>', methods=['GET'], strict_slashes=False)
def list_notif(user_id):
    """get a list of user notification"""
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/notif/<user_id>"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(user_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    notif_list = storage.get_all_user_notif(Notification, user_id)
    for notifs in notif_list:
        sender_user = storage.get(User, notifs["maker_user_id"])
        notifs["maker_full_name"] = sender_user.full_name
        notifs["maker_avatar"] = sender_user.user_avatar

    succ_dict = {}

    if len(notif_list) > 3:
        only_four = []
        for i in range(4):
            only_four.append(notif_list[i])
        succ_dict["data"] = only_four
    else:
        succ_dict["data"] = notif_list

    return make_response(jsonify(succ_dict), 200)

@app_views.route('/notif/<notif_id>', methods=['DELETE'], strict_slashes=False)
def delnotif(notif_id):
    """
    delete a notification
    """
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/notif/<user_id>"
    response_dict["error_code"] = "8"
    try:
        uuid_obj = UUID(notif_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    notif = storage.get(Notification, notif_id)
    if not notif:
        return make_response(jsonify(response_dict), 202)
    else:
        storage.delete(notif)
        storage.save()
        storage.reload()
        return make_response(jsonify({}), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)
