#!/usr/bin/python3
"""
The main API file.
"""

from flask import Flask
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


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host:
        host_value = host
    else:
        host_value = '0.0.0.0'
    if port:
        port_value = port
    else:
        port_value = '5000'
    app.run(host=host_value, port=port_value, threaded=True)
