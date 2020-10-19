#!/usr/bin/python3
"""
CrossMe Official API
Serving Information From BackeEnd To FrontEnd
"""

from flask import Flask, make_response, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config["IMAGE_UPLOADS"] = "./web_front/static/images/"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]


@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ 404 Error
    ---
    responses:
      404:
        description: a resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)



if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5002, ssl_context=('./ssl/server.crt', './ssl/server.key'), threaded=True)
