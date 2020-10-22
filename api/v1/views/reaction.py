#!/usr/bin/python3
""" API actions for Reactions """

from models.follow import Follow
from models.user import User
from models.post import Post
from models.reaction import Reaction
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify,request,abort
from uuid import UUID

@app_views.route('/like/<post_id>', methods=['POST'], strict_slashes=False)
def post_like(post_id):
    """
    make a like
    Return:dict of the recation id
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    f = storage.get(Post, post_id)
    if f is None:
        abort(404)
    #<source_user_id>/<target_user_id>
    mydata = request.get_json()
    new= Reaction()
    for k , v in mydata.items():
        setattr(new, k, v)
    new.save() 
    print(new)
    return make_response(jsonify(new.to_dict()), 201)

@app_views.route('/react/<post_id>/<current_user>', methods=['DELETE'], strict_slashes=False)
def delete_like(post_id, current_user):
    """
    Delete a like
    """
    if request.method == 'DELETE':
        react = storage.get_react(Reaction, post_id, current_user)
        react.delete()
        storage.save()
        storage.reload()
        return make_response (jsonify({}), 200)


@app_views.route('/like/<id>', methods=['DELETE'], strict_slashes=False)
def deletebyid(id):
    """deletebyid"""
    f = storage.get(Reaction, id)
    if f:
        storage.delete(f)
        storage.save()
        return jsonify({})
    else:
        abort(404)

@app_views.route('/like/<post_id>', methods=['GET'], strict_slashes=False)
def getreactions(post_id):
    """post reactions"""
    mypost = storage.get(Post, post_id)
    if not mypost:
        abort(404)
    userlist= []
    mydict={}
    for i in mypost.reactionlist:
        userlist.append(i.source_user_id)
    mydict["users"] = userlist
    return make_response(jsonify(mydict), 200)
    