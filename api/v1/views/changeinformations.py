#!/usr/bin/python3
""" API actions for Reactions """

from models.follow import Follow
from models.user import User
from models.post import Post
from models.tokens import Token
from models.reaction import Reaction
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify,request,abort
from uuid import UUID




@app_views.route('/changedata/', methods=['POST'], strict_slashes=False)
def change_user_informations():
    """
    change informations
    check token 
    Return: changed or not
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    storage.reload()
    mydata = request.get_json()
    a = storage.checkbysecurecode(mydata['user_id'], mydata['securecode'])
    if a is None:
        return make_response(jsonify({'error': 'Auth failed'}), 401)
    userobj = storage.get(User, mydata['user_id'])
    if not userobj:
        return make_response(jsonify({'error': 'No user found'}), 401)
    checkmail = storage.all(User)
    for i in checkmail.values():
        if i.email == mydata["email"] and i.email != userobj.email:
            return make_response(jsonify({'error': 'Email already used by another user.'}), 401)
    userobj.email=mydata["email"]
    userobj.full_name=mydata["name"]
    userobj.save()
    storage.delete(a)
    storage.save()
    return make_response(jsonify({'success': 'Done !'}), 201)