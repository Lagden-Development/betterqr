"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.

This is the main application file for the AR15 website. It contains the main application logic and configuration.
"""

# Import the required modules

# Third Party Modules
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

# Flask Modules
from flask import Flask

# Flask Extensions
from flask_minify import Minify

# Endpoints
from endpoints import main_endpoints

# Load the environment variables
load_dotenv()

# Create the Flask app and load extentions

# Flask App
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_port=1)

# Extensions
Minify(app)

# Custom Error Handlers


@app.errorhandler(404)
def page_not_found(_):
    return "The page you are looking for does not exist.", 404


# Sitemap


@app.route("/sitemap.xml")
def sitemap():
    with open("sitemap.xml") as sitemap_file:
        return sitemap_file.read(), 200, {"Content-Type": "application/xml"}


# Register the all the blueprints

app.register_blueprint(main_endpoints.blueprint)

# Run the built-in development server when ran as a script.
if __name__ == "__main__":
    app.run(
        debug=True,
        port=55444,
    )
