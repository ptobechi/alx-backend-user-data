#!/usr/bin/env python3
"""
Flask application setup
"""

from flask import Flask, jsonify, request, abort, make_response
from flask import redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """Registers a new user or returns an error
    if the user already exists."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        if AUTH.register_user(email, password):
            return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login_user():
    """Log in a user and create a session or return an error if login fails."""
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or not password:
        abort(400, description="Email and password are required")

    if not AUTH.valid_login(email, password):
        abort(401, description="Unauthorized")

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout_user():
    """Log out a user by destroying their session."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403, description="Forbidden")

    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        response = redirect("/")
        response.set_cookie("session_id", "", expires=0)
        return response

    abort(403, description="Forbidden")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
