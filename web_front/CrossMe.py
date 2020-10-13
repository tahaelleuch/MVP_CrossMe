#!/usr/bin/python3
""" Starts a Flask CrossMe app """

from flask import Flask, render_template
import uuid

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def crossme():
    """CrossMe is live"""
    return render_template('index.html', cache_id=uuid.uuid4())

if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
