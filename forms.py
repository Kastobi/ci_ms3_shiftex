from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from db import mongo

# todo: implement dynamic way after testing, some from one rotation plan for dev / testing
drugstoreList = [
    ("1735003", "Bären-Apotheke Bestenheid"),
    ("3000184", "Engel-Apotheke Frammersbach"),
    ("3000175", "Hubertus-Apotheke Marktheidenfeld"),
    ("3000033", "Stadt-Apotheke Stadtprozelten"),
    ("1735004", "Hof-Apotheke Wertheim")
]


class LoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])
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
                        validators=[DataRequired(),
                                    Email()])
    drugstore_id = SelectField("Drugstore",
                               choices=drugstoreList,
                               validators=[DataRequired()])
    password = PasswordField("Password",
                             validators=[DataRequired(),
                                         Length(min=6),
                                         Regexp("^(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{6,}$",
                                                message="""Minimum six characters, at least one letter, 
                                                one number and one special character.""")])
    password_confirm = PasswordField("Confirm Password",
                                     validators=[EqualTo("password"),
                                                 DataRequired()])
    agreed = BooleanField("Agree to Terms & Conditions and Privacy Policy",
                          validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    @staticmethod
    def validate_email(self, email):
        check_email = mongo.db.users.find_one({"email": email.data})
        if check_email is not None:
            raise ValidationError("Email is already taken! Please choose a different one or contact admin.")

    @staticmethod
    def validate_drugstore_id(self, drugstore_id):
        check_drugstore_id = mongo.db.users.find_one({"drugstoreId": int(drugstore_id.data)})
        if check_drugstore_id is not None:
            raise ValidationError("Drugstore is already taken! Please choose a different one or contact admin.")
