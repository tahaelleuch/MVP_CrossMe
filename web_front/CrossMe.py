#!/usr/bin/python3
""" Starts a Flask CrossMe app """

from flask import Flask, render_template, request, json, url_for, redirect,flash, session
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
import uuid
from models import storage
from models.user import User

app = Flask(__name__)

"""
@app.teardown_appcontext
def teardo_db(session):
    models.storage.close()
"""


@app.route('/')
def home():
    if "email" in session:
        email = session['email']
        return render_template('home.html', cache_id=uuid.uuid4(), user=email)
    return render_template('index.html', cache_id=uuid.uuid4())


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
                return render_template('home.html', cache_id=uuid.uuid4(), user=request.form['email'])
            else:
                return render_template('index.html', cache_id=uuid.uuid4(), error="Invalid Details")
        else:
            return render_template('index.html', cache_id=uuid.uuid4(), error="Missing information")
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
        new.auth= True
        session['email'] = request.form['email']
        new.save()
        print(session)
        return render_template('home.html', cache_id=uuid.uuid4(), user=request.form['email'])
    else:
        return render_template('index.html', cache_id=uuid.uuid4())



if __name__ == "__main__":
    app.secret_key = 'foued'
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
