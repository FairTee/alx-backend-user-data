#!/usr/bin/env python3
"""
Module for Flask app
"""
from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.session_exp_auth import SessionExpAuth

app = Flask(__name__)
app.register_blueprint(app_views)

auth = None
if getenv('AUTH_TYPE') == 'session_exp_auth':
    auth = SessionExpAuth()

@app.before_request
def before_request():
    """Method to handle before request actions"""
    if auth is not None:
        request.current_user = auth.current_user(request)

@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error):
    """Handler for 401 errors"""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error):
    """Handler for 403 errors"""
    return jsonify({"error": "Forbidden"}), 403

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = int(getenv("API_PORT", "5000"))
    app.run(host=host, port=port)
