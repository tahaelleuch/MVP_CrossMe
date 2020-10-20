#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Posts

    Error codes:
        0: unknown error
        9: invalid path
        8: invalid parameter
        7: invalid request
        6: invalid file format
"""

from models.post import Post
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request, session
from uuid import UUID
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from api.v1.app import app



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
        if not valid file format:
            error code 6
        if success:
            return success code 200
        else
            unknown error (code : 0)
    """
    if request.method == 'POST':


        response_dict = {}
        response_dict["error"] = "invalid parameter"
        response_dict["usage"] = "/post/new"
        response_dict["error_code"] = "8"

        try:
            uuid_obj = UUID(user_id, version=4)
        except ValueError:
            return make_response(jsonify(response_dict), 202)

        user = storage.get(User, user_id)
        if not user:
            return make_response(jsonify(response_dict), 202)
        if not request.files and not request.form:
            invalid_dict = {}
            invalid_dict["error"] = "invalid request"
            invalid_dict["usage"] = "/post/<user_id>/new"
            invalid_dict["required_methods"] = "POST"
            invalid_dict["error_code"] = "7"
            return make_response(jsonify(invalid_dict), 202)
        else:
            new_post = Post()
            if request.form:
                from_data = request.form.to_dict()

                new_post.post_text = from_data["data"]
            else:
                new_post.post_text = "NULL"

            if request.files:
                new_post.post_type = "IMAGE"
                image = request.files['file']

                if "." in image.filename:
                    ext = image.filename.split(".")[-1]
                    if ext.upper() not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                        invalid_dict = {}
                        invalid_dict["error"] = "invalid file format"
                        invalid_dict["usage"] = "/post/<user_id>/new"
                        invalid_dict["required_methods"] = "POST"
                        invalid_dict["error_code"] = "6"
                        return make_response(jsonify(invalid_dict), 202)
                else:
                    invalid_dict = {}
                    invalid_dict["error"] = "invalid file format"
                    invalid_dict["usage"] = "/post/<user_id>/new"
                    invalid_dict["required_methods"] = "POST"
                    invalid_dict["error_code"] = "6"
                    return make_response(jsonify(invalid_dict), 202)

                new_filename = 'cm_' + str(new_post.id) + '.' + ext
                final_filename = secure_filename(new_filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], final_filename))
                final_path = '/static/images/' + final_filename

                new_post.media_url = final_path

            new_post.user_id = user_id
            new_post.creation_date = datetime.utcnow()
            new_post.post_source = "CROSSME"
            new_post.save()
            storage.reload()

            my_user = user.to_dict()
            my_post = new_post.to_dict()

            my_post["user_full_name"] = my_user["full_name"]
            my_post["user_avatar"] = my_user["user_avatar"]

            if not my_post["post_text"] or my_post["post_text"] == "NULL":
                my_post["post_text"] = ""


            if "media_url" not in my_post.keys():
                my_post["media_url"] = "nomedia"

            storage.reload()
            return make_response(jsonify(my_post), 200)

    unknown_dict = {}
    unknown_dict["error"] = "unknown error"
    unknown_dict["error_code"] = "0"
    return make_response(jsonify(unknown_dict), 404)


@app_views.route('/friendposts/<user_id>/<page_num>', methods=['GET'], strict_slashes=False)
def get_friend_posts(user_id, page_num=0):
    """
    get list of friend post
    Args:
        user_id : current user connected id
    Return:

    """
    response_dict = {}
    response_dict["error"] = "invalid parameter"
    response_dict["usage"] = "/post/<post_id>"
    response_dict["error_code"] = "8"

    try:
        uuid_obj = UUID(user_id, version=4)
    except ValueError:
        return make_response(jsonify(response_dict), 202)

    user = storage.get(User, user_id)
    if not user:
        return make_response(jsonify(response_dict), 202)

    user_follows = user.follow_list()

    if not user_follows:
        return make_response(jsonify({}), 200)

    friends_posts = []
    for friend_id in user_follows:
        post_lst = storage.getlist_by_attr(Post, friend_id)
        friends_posts = friends_posts + post_lst

    if not friends_posts:
        return make_response(jsonify({}), 200)

    sorted_post_list = storage.sort_posts(friends_posts)

    ten_post = []
    index = 10 * int(page_num)

    for i in range(10):
        if len(sorted_post_list) < index + 1:
            break
        post = sorted_post_list[index]
        friend_profile_obj = storage.get(User, post["user_id"])
        friend_profile = friend_profile_obj.to_dict()
        post["full_name"] = friend_profile["full_name"]
        post["user_avatar"] = friend_profile["user_avatar"]
        if post["post_text"] == "NULL":
            post["post_text"] = " "
        if post["media_url"] is None:
            post["media_url"] = "nomedia"
        ten_post.append(post)
        index = index + 1


    such_dict = {}
    such_dict["data"] = ten_post
    return make_response(jsonify(such_dict), 200)

