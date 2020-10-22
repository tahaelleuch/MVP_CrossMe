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




@app_views.route('/changerequest/', methods=['POST'], strict_slashes=False)
def changeme():
    """
    change password
    check token 
    Return: changed or not
    """
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    storage.reload()
    mydata = request.get_json()
    print(mydata)

    a = storage.checkbysecurecode(mydata['user_id'], mydata['securecode'])
    if a is None:
        return make_response(jsonify({'error': 'Auth failed'}), 401)
    userobj = storage.get(User, mydata['user_id'])
    b = userobj.as_dict()
    verif = User().verify_password(mydata['password'], b["password"])
    if not verif:
        return make_response(jsonify({'error': 'false pwd'}), 401)
    n= userobj.hashpwd(mydata['newpwd'])
    userobj.password=n
    userobj.save()
    a.delete()
    return make_response(jsonify(userobj.to_dict()), 201)