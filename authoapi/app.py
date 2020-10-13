#!/usr/bin/python3
"""authentification api"""
import models
from authoapi.views import app_views
from flask import Flask, make_response, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app)


@app.teardown_appcontext
def teardo_db(session):
    """close session"""
    models.storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port= '5009', threaded=True)