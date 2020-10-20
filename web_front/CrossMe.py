#!/usr/bin/python3
""" Starts a Flask CrossMe app """

from flask import Flask, render_template, request, json, url_for, redirect, flash, session
from flask import make_response, jsonify
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
import uuid
from models import storage
from models.user import User
from models.post import Post
from models.follow import Follow
from flask_cors import CORS
import requests as rq

app = Flask(__name__)
cors = CORS(app)

@app.errorhandler(404)
def resource_not_found(e):
    return  render_template('404.html'), 404




@app.route('/')
def home():
    if "email" in session:
        email = session['email']
        return render_template('home.html', cache_id=uuid.uuid4(), user=email)
    return render_template('index.html', cache_id=uuid.uuid4())


@app.route('/profile/<user_id>', strict_slashes=False)
def render_profile(user_id):
    """
    Render The profile page
    if user doesn't exist or invalid id redirect to home

    """
    try:
        uuid_obj = uuid.UUID(user_id, version=4)
    except ValueError:
        return redirect('/')
    storage.reload()
    user = storage.get(User, user_id)
    user_info = user.to_dict()

    all_user_post = storage.getlist_by_attr(Post, user_id)

    number_of_followers = storage.follower_number(Follow, user_id)

    if "email" in session:

        current_user_email = session['email']

        if user_info["email"] == current_user_email:
            follow_code = "3"
            return render_template('profile.html',
                                   cache_id=str(uuid.uuid4()),
                                   user_info=user_info,
                                   all_user_post=all_user_post,
                                   is_user="ok",
                                   follow_code=follow_code,
                                   number_of_followers=number_of_followers)

        else:
            my_current_user = storage.getbyemail(User, current_user_email)
            current_user_id = my_current_user.id
            follow_obj = storage.get_by_two(Follow, current_user_id, user_id)
            if follow_obj:
                follow_code = str(follow_obj.follow_code)
                if follow_code != "0":
                    rev_obj = storage.get_by_two(Follow, user_id, current_user_id)
                    if rev_obj:
                        if follow_obj.follow_code == 1 and rev_obj.follow_code == 1:
                            follow_code == "1"
                        elif rev_obj.follow_code == 1:
                            follow_code = "2"
            else:
                follow_code = "0"
                rev_obj = storage.get_by_two(Follow, user_id, current_user_id)
                if rev_obj:
                    if follow_obj:
                        if follow_obj.follow_code == 1 and rev_obj.follow_code == 1:
                            follow_code == "1"
                        elif rev_obj.follow_code == 1:
                            follow_code = "2"
                    else:
                        follow_code = "2"


            print (follow_code)
            return render_template('profile.html',
                                   cache_id=str(uuid.uuid4()),
                                   user_info=user_info,
                                   all_user_post=all_user_post,
                                   is_user="notok",
                                   follow_code=follow_code,
                                   number_of_followers=number_of_followers)

    return render_template('profile.html',
                           cache_id=str(uuid.uuid4()),
                           user_info=user_info,
                           all_user_post=all_user_post,
                           is_user="notok",
                           follow_code="9",
                           number_of_followers=number_of_followers)


@app.route('/me', strict_slashes=False)
def render_me():
    """
    Render The profile page
    User will be redirected by it id to his profile
    """
    if "email" in session:
        user_email = session['email']
        me_user = storage.getbyemail(User, user_email)
        user_id = me_user.id
        NEWURL = '/profile/' + user_id
        return redirect(NEWURL)
    else:
        redirect('/')



@app.route('/login',methods=['GET', 'POST'])
def logg():
    if request.method == 'POST':
        if request.form['email'] and request.form['password']:
            req_data = request.form.to_dict()
            users = storage.getbyemail(User, request.form['email'])
            if users is None:
                return render_template('index.html', cache_id=uuid.uuid4(), error="Invalid Details")
            a = users.as_dict()
            print(a)
            print(a.__class__.__name__)
            b = User().verify_password(req_data['password'], a["password"])
            if b:
                session['email'] = request.form['email']
                if not a["fb_access_token"] and not a["ig_access_token"]:
                    return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=session['email'])
                elif not a["fb_access_token"] and not a["ig_access_token"]:
                    return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=session['email'])
                else:
                    return render_template('home.html', cache_id=uuid.uuid4(), user=session['email'])
            else:
                return render_template('index.html', cache_id=uuid.uuid4(), error="Invalid Details")
        else:
            return render_template('index.html', cache_id=uuid.uuid4(), error="Missing information")
    else:
        if session:
            storage.reload()
            user_info = storage.getbyemail(User, session['email']).as_dict_nopwd()
            if not user_info["fb_access_token"] and not user_info["ig_access_token"]:
                return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=user_info)
            elif not user_info["fb_access_token"] or not user_info["ig_access_token"]:
                return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=user_info)
            else:
                return render_template('home.html', cache_id=uuid.uuid4(), user=session['email'])
        else:
            return render_template('index.html', cache_id=uuid.uuid4())


@app.route('/logout',methods=['GET', 'POST'])
def loggoo():
        session.pop('email', None)
        return render_template('index.html', cache_id=uuid.uuid4())


@app.route('/register',methods=['GET', 'POST'])
def signUp():
    """create  users"""
    if request.method == 'POST':
        f = request.form['full_name']
        e = request.form['email']
        p = request.form['password']
        if not e and not f and not p:
            return render_template('index.html', cache_id=uuid.uuid4(), error="Missing information")
        all_cls = storage.all(User)
        for value in all_cls.values():
            if (value.email == e):
                return render_template('index.html', cache_id=uuid.uuid4(), error="Already Registred")
        req_data = request.form.to_dict()
        new= User()
        for k , v in req_data.items():
            if k == "password":
                v = new.hashpwd(v)
            setattr(new, k, v)
        setattr(new, "user_avatar", '/static/images/default-user-image.png')
        new.auth = True
        session['email'] = request.form['email']
        new.save()
        my_user = storage.getbyemail(User, request.form['email'])
        return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info= my_user)
    else:
        if session:
            storage.reload()
            user_info = storage.getbyemail(User, session['email']).as_dict_nopwd()
            if not user_info["fb_access_token"] and not user_info["ig_access_token"]:
                return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=user_info)
            elif not user_info["fb_access_token"] or not user_info["ig_access_token"]:
                return render_template('steptwo.html', cache_id=uuid.uuid4(), user_info=user_info)
            else:
                return render_template('home.html', cache_id=uuid.uuid4(), user=session['email'])
        else:
            return render_template('index.html', cache_id=uuid.uuid4())


@app.route('/search/',methods=['GET', 'POST'])
def CMsearch():
    if "email" in session:
        if request.method == "POST":
            pattern = request.form['pt']
            if len(pattern) is None or len(pattern) > 25:
                return render_template('search.html', cache_id=uuid.uuid4(), result=[])
            if "@" in pattern:
                my_user = storage.getbyemail(User, pattern)
                if my_user:
                    return render_template('search.html', cache_id=uuid.uuid4(), result=my_user)
                else:
                    return render_template('search.html', cache_id=uuid.uuid4(), result=[])
            strsplitted = pattern.split()
            allusers =  storage.all(User)
            my_list = []
            for i in allusers.values():
                if i.full_name == pattern:
                    my_list.append(i)
                else:
                    for j in strsplitted:
                        if j in i.full_name.split():
                            my_list.append(i)
            return render_template('search.html', cache_id=uuid.uuid4(), result=my_list)
        return render_template('search.html', cache_id=uuid.uuid4(), result=[])
    else:
        return redirect('/')


@app.route('/flw/<followed_id>',methods=['POST'])
def make_follow(followed_id):
    """send request to the api to make a follow"""
    if request.method == "POST":
        if "email" in session:
            user_email = session['email']
            user_obj = storage.getbyemail(User, user_email)
            follower_id = user_obj.id
            response = rq.post('https://0.0.0.0:5002/api/v1/new_follow/' +
                               follower_id + '/' + followed_id + '/onetwo', verify=False)
            succ = {}
            succ["status"] = "ok"
            return make_response(jsonify(succ), 200)
    return redirect('/profile/' + followed_id)


@app.route('/flw/<followed_id>',methods=['DELETE'])
def del_follow(followed_id):
    """send request to the qpi to delet a follow"""
    if request.method == "DELETE":
        if "email" in session:
            user_email = session['email']
            user_obj = storage.getbyemail(User, user_email)
            follower_id = user_obj.id
            response = rq.delete('https://0.0.0.0:5002/api/v1/del_follow/' +
                               follower_id + '/' + followed_id + '/onetwo', verify=False)
            succ = {}
            succ["status"] = "ok"
            return make_response(jsonify(succ), 200)
    return redirect('/profile/' + followed_id)


if __name__ == "__main__":
    app.secret_key = 'mycrossme'
    """ Main Function """
    app.run(host='0.0.0.0', port=5000, ssl_context=('./ssl/server.crt', './ssl/server.key'))
