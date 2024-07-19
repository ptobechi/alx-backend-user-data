#!/usr/bin/env python3
"""
Flask application setup
"""

from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Returns a JSON response with a welcome message."""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"])
def register_user():
    """Registers a new user or returns an error if the user already exists."""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password are required"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
