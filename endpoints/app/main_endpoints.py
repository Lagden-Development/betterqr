"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.

This is the main endpoints file for the website. It contains the main endpoints for the website and their
associated logic.
"""

# Import the required modules

# Flask Modules
from flask import (
    Blueprint,
    session,
    redirect,
)

# Create a Blueprint for main routes
blueprint = Blueprint("app_main", __name__, url_prefix="/app")

# Route Endpoints


@blueprint.route("/")
def _index():
    if "sid" not in session:
        return redirect(
            "/login?utm_source=internal&utm_medium=redirect&utm_campaign=login_redirect&utm_content=not_logged_in"
        )

    return "Welcome to the app!"
