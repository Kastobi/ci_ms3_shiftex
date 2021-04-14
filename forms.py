from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    first_name = StringField("First Name",
                             validators=[DataRequired()])
    last_name = StringField("Last Name",
                            validators=[DataRequired()])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password",
                                     validators=[EqualTo("password"), DataRequired()])
    agreed = BooleanField("Agree to Terms & Conditions and Privacy Policy",
                          validators=[DataRequired()])
    submit = SubmitField("Sign Up")
