#!/usr/bin/python3
""" Starts a Flask CrossMe app """

from flask import Flask, render_template, request, json, url_for, redirect,flash
from flask_login import LoginManager, UserMixin, login_required, login_user, current_user
import uuid

app = Flask(__name__)




@app.route('/', strict_slashes=False, methods=['GET'])
def home():
    return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/login',methods=['GET', 'POST'])
def logg():
    if request.method == 'POST':
        """CrossMe is live"""
        return "hello"
    else:
        return render_template('index.html', cache_id=uuid.uuid4())

@app.route('/register',methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        """CrossMe is live"""
        return "register"
    else:
        return render_template('index.html', cache_id=uuid.uuid4())



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
