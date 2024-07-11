#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
import os
from api.v1.auth.session_exp_auth import SessionExpAuth
from api.v1.auth.session_db_auth import SessionDBAuth
from models import db_session


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

AUTH_TYPE = os.getenv("AUTH_TYPE", "session_auth")

if AUTH_TYPE == "basic_auth":
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    auth = SessionDBAuth()
else:
    auth = None

EXCLUDED_PATHS = ['/api/v1/auth_session/login/']


@app.before_request(401)
def before_request(error) -> str:
    """
    Before request handler to authenticate and authorize requests.
    """
    path = request.path

    if auth.authorization_header(
        request) is None and auth.session_cookie(request) is None:
        abort(401)

    if path not in EXCLUDED_PATHS and auth.require_auth(path,
                                                        EXCLUDED_PATHS
                                                        ):
        if auth.authorization_header(
            request) is None and auth.session_cookie(request) is None:
            abort(401)


def random_authorization_check(user):
    """
    Simulated random authorization check.
    Replace this with your actual authorization logic.
    """
    import random
    return random.choice([True, False])


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
