"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Python Standard Library
import os

# Third Party Modules
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Import the custom logger and setup function
from logger import QRLOG_DB, setup_betterqr_logging

# Load the environment variables
load_dotenv()

# Ensure logging is configured
setup_betterqr_logging()

uri = os.getenv("mongodb_uri")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    QRLOG_DB.info("Successfully connected to the MongoDB server")
except Exception as e:
    QRLOG_DB.error(f"Failed to connect to the MongoDB server: {e}")
    exit(1)

QRLOG_DB.info("Database connection established.")
QRLOG_DB.info("Creating links to the databases and collections.")

# Create links to the databases and collections
betterqr_db = client["betterqr"]

# Create a collection for the users
users_collection = betterqr_db["users"]

# Log the successful creation of the links
QRLOG_DB.info("Links to the databases and collections created.")
QRLOG_DB.info("Database setup complete.")
