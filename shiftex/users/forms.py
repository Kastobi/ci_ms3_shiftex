"""
shiftex users package - forms module
====================================

Containing Login and Registration Form and the validators

classes:
    LoginForm
    RegistrationForm
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp

from shiftex.main import mongo


class LoginForm(FlaskForm):
    """
    Login Form for /login route
    """
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])
    password = PasswordField("Password",
                             validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """
    Registration Form for /register route with validators for fundamental fields,
    providing user-feedback if validation is not possible

    validator:
        email, drugstore_id: checks users collection if email or drugstore are already registered
        password: sets minimal password security
        password_confirm: to prevent typos in password
    """
    first_name = StringField("First Name",
                             validators=[DataRequired()])
    last_name = StringField("Last Name",
                            validators=[DataRequired()])
    email = StringField("Email",
                        validators=[DataRequired(),
                                    Email()])
    drugstore_id = SelectField("Drugstore sorted by rotation plan",
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

    def __init__(self, *args, **kwargs):
        """
        Query for Drugstores to choose from
        Builds distinct list of drugstore ids and removes taken ones
        """
        # https://stackoverflow.com/questions/28133859/how-to-populate-wtform-select-field-using-mongokit-pymongo"
        drugstore_list = list(mongo.db.shifts.aggregate([
            {"$group":
                 {"_id": "$drugstoreId",
                  "digits": {"$first": "$digits"},
                  "drugstoreName": {"$first": "$drugstore.name"}
                  }},
            {"$project": {
                "_id": 0,
                "drugstoreId": "$_id",
                "digits_with_name":
                    {"$concat": [
                        "$digits",
                        " ",
                        "$drugstoreName"
                    ]}
            }}
        ]))
        taken_drugstores = mongo.db.users.distinct("drugstoreId")
        drugstore_choices = [(item["drugstoreId"], item["digits_with_name"]) for item in drugstore_list
                             if not item["drugstoreId"] in taken_drugstores]
        drugstore_choices.sort(key=lambda tup: tup[1])

        self.drugstore_id.kwargs["choices"] = drugstore_choices
        super().__init__()

    def validate_email(self, email: StringField):
        """
        Checks if there is a user with given email
        """
        check_email = mongo.db.users.find_one({"email": email.data.lower()})
        if check_email is not None:
            raise ValidationError("Email is already taken! Please choose a different one or contact admin.")

    def validate_drugstore_id(self, drugstore_id: SelectField):
        """
        Checks if there is a user with given drugstore
        """
        check_drugstore_id = mongo.db.users.find_one({"drugstoreId": int(drugstore_id.data)})
        if check_drugstore_id is not None:
            raise ValidationError("Drugstore is already registered! Please choose a different one or contact admin.")
