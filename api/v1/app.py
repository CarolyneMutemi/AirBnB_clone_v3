#!/usr/bin/python3
"""
The main API file.
"""

import os
from flask_cors import CORS
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")


@app.teardown_appcontext
def refresh(exception):
    """
    Called after every request.
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Error page.
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True, threaded=True)
