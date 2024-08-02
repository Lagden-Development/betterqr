"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Flask Modules
from flask import Blueprint, jsonify

# Create a Blueprint for main routes
blueprint = Blueprint("api_users", __name__, url_prefix="/api/users")

# Route Endpoints


@blueprint.route("/")
def _index():
    return jsonify({"ok": True, "status": "betterqr.app api"}), 200
