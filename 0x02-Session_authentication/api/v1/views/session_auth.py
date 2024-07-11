#!/usr/bin/env python3
"""
Session Authentication View

This module handles session-based authentication for the API.
Routes:
- POST /api/v1/auth_session/login:
Handles user login and session creation.
"""

from flask import request, jsonify, abort
from api.v1.app import auth
from models.user import User
import os


def login():
    """ Handle user login and session creation """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user from database
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    # Validate password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session and set cookie
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)

    return response

def logout():
    """ Handle user logout """
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({}), 200