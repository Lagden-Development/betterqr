"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.

This is the main endpoints file for the website. It contains the main endpoints for the website and their
associated logic.
"""

# Import the required modules

# Python Standard Library
import os

# Flask Modules
from flask import Blueprint, render_template, session, redirect

# Forms
from forms.login import LoginForm
from forms.signup import SignupForm

# Database
from helpers.db import users_collection

# Create a Blueprint for main routes
blueprint = Blueprint("main", __name__, url_prefix="/")

# Context Processors


@blueprint.context_processor
def inject_recaptcha_details():
    return {
        "recaptcha_site_key": os.getenv("recaptcha_site_key"),
    }


# Route Endpoints


@blueprint.route("/")
def _index():
    return render_template("index.html")


@blueprint.route("/signup")
def _signup():
    form = SignupForm()
    return render_template("login_signup/signup.html", form=form)


@blueprint.route("/login")
def _login():
    form = LoginForm()
    return render_template("login_signup/login.html", form=form)


@blueprint.route("/logout")
def _logout():
    if "sid" not in session:
        return redirect(
            "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_already"
        )

    sid = session["sid"]

    # Assusimg the sid is stored in the database within a user document in the
    # users collection, the sid will be in one of the users "sessions" array

    query = users_collection.find_one({"sessions.sid": sid})

    if query is None:
        return redirect(
            "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_invalid_sid"
        )

    if not isinstance(query, dict):
        return redirect(
            "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_error"
        )

    # Add the session to the "logged_out_sessions" array (if it exists, otherwise create it)
    if "logged_out_sessions" not in query:
        users_collection.update_one(
            {"uuid": query["uuid"]},
            {"$set": {"logged_out_sessions": [query["sessions"][0]]}},
        )
    else:
        users_collection.update_one(
            {"uuid": query["uuid"]},
            {"$push": {"logged_out_sessions": query["sessions"][0]}},
        )

    # Create an index to delete any logged out sessions that are older than 30 days
    # Every session has a "created_at" field that is a datetime object in UTC

    # Ensure the index does not already exist
    if not "logged_out_sessions.created_at_1" in users_collection.index_information():
        # Create the index
        users_collection.create_index(
            [("logged_out_sessions.created_at", 1)],
            expireAfterSeconds=2592000,  # 30 days
        )

    # Remove the session from the "sessions" array
    users_collection.update_one(
        {"uuid": query["uuid"]},
        {"$pull": {"sessions": {"sid": sid}}},
    )

    # Remove the session from the session cookie
    session.pop("sid")

    # Redirect the user to the home page
    return redirect(
        "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out"
    )


@blueprint.route("/terms")
def _terms():
    return render_template("policies/terms.html")


@blueprint.route("/privacy")
def _privacy():
    return render_template("policies/privacy.html")
