#!/usr/bin/python3
"""status"""
from flask import Flask, jsonify
from authoapi.views import app_views


app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    pass