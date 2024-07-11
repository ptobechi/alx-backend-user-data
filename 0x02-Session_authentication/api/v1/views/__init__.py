#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from api.v1.views.session_auth import login, logout

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.users import *

# Register session_auth views
app_views.route('/auth_session/login', methods=['POST'])(login)
app_views.route('/auth_session/logout', methods=['DELETE'])(logout)

# Ensure the blueprint is registered with the Flask app
from api.v1.app import app
app.register_blueprint(app_views)

User.load_from_file()
