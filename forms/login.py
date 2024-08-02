"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Third Party Modules
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField
from wtforms.validators import DataRequired, Email


# Create the login form
class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
