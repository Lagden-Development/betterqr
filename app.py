"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Python Standard Library
import datetime
import logging
import os

# Third Party Modules
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

# Flask Modules
from flask import Flask, request, session, redirect, flash

# Flask Extensions
from flask_session import Session
from flask_minify import Minify

# Database
from db import client as db_client, users_collection

# Endpoints
from endpoints import main_endpoints
from endpoints.app import main_endpoints as app_main_endpoints
from endpoints.api import (
    forms_endpoints as api_forms_endpoints,
    users_endpoints as api_users_endpoints,
)

# Import the custom logger and setup function
from logger import QRLOG_REQUESTS, setup_betterqr_logging

# Load the environment variables
load_dotenv()

# Create the Flask app and load extensions

# Flask App
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1)

# Flask Configuration

app.config["SECRET_KEY"] = os.getenv("secret_key")
app.config["SESSION_COOKIE_SECURE"] = True

app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = db_client
app.config["SESSION_MONGODB_DB"] = os.getenv("mongodb_db")
app.config["SESSION_MONGODB_COLLECTION"] = os.getenv("mongodb_session_collection")

app.config["RECAPTCHA_USE_SSL"] = True
app.config["RECAPTCHA_PUBLIC_KEY"] = os.getenv("recaptcha_site_key")
app.config["RECAPTCHA_PRIVATE_KEY"] = os.getenv("recaptcha_secret_key")
app.config["RECAPTCHA_OPTIONS"] = {"theme": "white"}


# Extensions
Minify(app)
Session(app)

# Setup custom logging
setup_betterqr_logging()


# Custom Error Handlers
@app.errorhandler(404)
def page_not_found(_):
    return "The page you are looking for does not exist.", 404


# Sitemap
@app.route("/sitemap.xml")
def sitemap():
    with open("sitemap.xml") as sitemap_file:
        return sitemap_file.read(), 200, {"Content-Type": "application/xml"}


# Register all the blueprints

# Normal Endpoints
app.register_blueprint(main_endpoints.blueprint)

# App Endpoints
app.register_blueprint(app_main_endpoints.blueprint)

# API Endpoints
app.register_blueprint(api_users_endpoints.blueprint)
app.register_blueprint(api_forms_endpoints.blueprint)


# Log requests
@app.after_request
def log_response_info(response):
    # Assuming the real address the "CF-Connecting-IP" header that cloudfare sends
    real_addr = request.headers.get("CF-Connecting-IP", "Unknown")

    extra_info = {
        "method": request.method,
        "path": request.path,
        "addr": request.remote_addr,
        "real_addr": real_addr,
        "status": response.status,
    }
    QRLOG_REQUESTS.info("Response logged", extra=extra_info)
    return response


# Ensure session
@app.before_request
def ensure_session():
    if "sid" not in session:
        return

    query = users_collection.find_one({"sessions.sid": session["sid"]})

    if query is None:
        session.pop("sid")
        flash("Your session has expired. Please log in again.", "warning")
        return redirect(
            "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_invalid_sid"
        )

    if not isinstance(query, dict):
        session.pop("sid")
        flash("An error occurred. Please log in again, or contact support.", "danger")
        return redirect(
            "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_error"
        )

    # Check if the session is more than 30 days old
    for session_data in query["sessions"]:
        if session_data["sid"] == session["sid"]:
            session_start = datetime.datetime.fromisoformat(session_data["created_at"])
            if (datetime.datetime.now() - session_start).days >= 30:
                session.pop("sid")
                flash("Your session has expired. Please log in again.", "warning")
                return redirect(
                    "/?utm_source=internal&utm_medium=redirect&utm_campaign=home_redirect&utm_content=logged_out_session_expired"
                )


# Disable the werkzeug logger
log = logging.getLogger("werkzeug")
log.disabled = True

# Run the built-in development server when run as a script.
if __name__ == "__main__":
    app.run(
        debug=True,
        port=55444,
    )
