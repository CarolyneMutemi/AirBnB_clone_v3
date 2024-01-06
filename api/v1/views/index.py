#!/usr/bin/python3
"""
Has the blueprint functions.
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', strict_slashes=False)
def status():
    """
    Returns a JSON showing the app status.
    """
    return jsonify({'status': 'OK'})
