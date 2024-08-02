"""
(c) 2024 Zachariah Michael Lagden (All Rights Reserved)
You may not use, copy, distribute, modify, or sell this code without the express permission of the author.
"""

# Import the required modules

# Third Party Modules
from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, StringField
from wtforms.validators import DataRequired, Email, EqualTo


# Create the login form
class SignupForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
