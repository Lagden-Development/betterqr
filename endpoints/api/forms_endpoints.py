"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Python Standard Library
import datetime
import uuid
import os

# Third Party Modules
from werkzeug.security import check_password_hash
import requests

# Flask Modules
from flask import Blueprint, jsonify, session, request

# Database Modules
from db import users_collection

# Forms
from forms.login import LoginForm
from forms.signup import SignupForm

# Create a Blueprint for main routes
blueprint = Blueprint("api_forms", __name__, url_prefix="/api/forms")

# Route Endpoints


@blueprint.route("/login", methods=["POST"])
def _login():
    form = LoginForm(request.form)

    if not form.validate_on_submit():
        return jsonify({"ok": False, "errors": form.errors}), 400

    recaptcha_response = request.form.get("g-recaptcha-response")
    data = {
        "secret": os.getenv("recaptcha_secret_key"),
        "response": recaptcha_response,
        "remoteip": request.headers.get("CF-Connecting-IP", request.remote_addr),
    }
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify", data=data
    )
    result = response.json()

    if not result["success"]:
        return (
            jsonify(
                {
                    "errors": {
                        "recaptcha": [
                            "Recaptcha verification failed. Please try again."
                        ]
                    }
                }
            ),
            400,
        )

    query = users_collection.find_one({"email": form.email.data})

    if query is None:
        return jsonify({"ok": False, "errors": {"email": ["User not found."]}}), 404

    if not isinstance(query, dict):
        return jsonify({"ok": False, "errors": {"internal": ["Database error."]}}), 500

    # Check if the password is correct

    if not check_password_hash(query["security"]["password"], form.password.data):
        return (
            jsonify({"ok": False, "errors": {"password": ["Incorrect password."]}}),
            401,
        )

    # Create a new session

    new_session = {
        "sid": str(uuid.uuid4()),
        "created_at": datetime.datetime.now(datetime.UTC),
        "ip": request.headers.get("CF-Connecting-IP", request.remote_addr),
        "user_agent": request.headers.get("User-Agent"),
    }

    # Update the user's sessions

    users_collection.update_one(
        {"uuid": query["uuid"]},
        {"$push": {"sessions": new_session}},
    )

    session["sid"] = new_session["sid"]

    return jsonify({"ok": True, "message": "Logged in successfully."}), 200
