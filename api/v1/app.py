#!/usr/bin/python3
"""
The main API file.
"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)

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
    return jsonify({"error": "Not found"})



if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, debug=True, threaded=True)
