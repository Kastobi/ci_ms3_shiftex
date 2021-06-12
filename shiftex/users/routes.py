"""
shiftex users package - routes module
=====================================

Provides the views for user management and
logged in users.

routes:
    /login
        -> GET -> login.html
        -> POST -> validates login form, logs user in
    /logout
        -> logs user out, redirect to index
    /register
        -> GET -> register.html
        -> POST -> validates register form, registers user
    /user

"""

import datetime

from bson import ObjectId
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from shiftex.main import mongo
from shiftex.users import bcrypt, users
from shiftex.main.filters import duration_to_readable
from shiftex.users.forms import LoginForm, RegistrationForm
from shiftex.users.models import User


@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Login user if email and password hash match an existing user in users collection
    """
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))

    form = LoginForm()

    if form.validate_on_submit():
        check_user = mongo.db.users.find_one({"email": form.email.data.lower()})
        if check_user and bcrypt.check_password_hash(check_user["passwordHash"], form.password.data):
            user = User(check_user)
            login_user(user, remember=form.remember.data)
            flash("Login successful!")
            return redirect(url_for("users.user"))
        else:
            flash("Login failed! Please check email and password.")

    return render_template("login.html", form=form)


@login_required
@users.route("/logout")
def logout():
    """Log user out"""
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))
    logout_user()
    flash(f"Logout successful!")
    return redirect(url_for("main.index"))


@users.route("/register", methods=["GET", "POST"])
def register():
    """
    register user on validated register form
    """
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        User.register_user(form.first_name.data,
                           form.last_name.data,
                           form.email.data.lower(),
                           form.drugstore_id.data,
                           hashed_password)
        flash(f"Registration complete for {form.first_name.data} {form.last_name.data}.")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@login_required
@users.route("/user")
def user():
    """
    Provide main functionality for logged in user.
    Uses the user document to identify relevant drugstore and rotation.
    The user.html is rendered once by the server and afterwards updated with jQuery

    Therefore:
        a) provide for the user relevant shifts (relevant = limit same time yesterday, 24h shifts!)
            -> filtering template (yesterday_stamp)
        b) provide all user-shifts in the current plan
            -> via drugstore identifier in shifts collection (users_shifts_list)
        c) provide all swap requests in the users rotation
            -> via rotation identifier in swaps collection (rotation_swaps_list)
        d) provide all swap requests posted by the user
            -> via shift ids in swaps and shifts lists
        e) checks if there are accepted offers to confirm (and therefore execute swap)
            -> users shifts ids vs ids in accept array in swap documents

    """
    if not current_user.is_authenticated:
        return redirect(url_for("main.index"))

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    yesterday_stamp = yesterday.timestamp() * 1000
    drugstore_id = current_user.drugstoreId
    users_shifts_list = list(mongo.db.shifts.find(
        {"drugstoreId": drugstore_id}
    ))
    rotation_swaps_list = list(mongo.db.swaps.find(
        {"digitsId": users_shifts_list[0]["digitsId"]}
    ))

    rotation_swap_requests_ids = []
    for rotation_swap_request in rotation_swaps_list:
        rotation_swap_requests_ids.append(ObjectId(rotation_swap_request["shiftId"]))

    users_shifts_ids = []
    for users_shift in users_shifts_list:
        users_shifts_ids.append(users_shift["_id"].__str__())

    rotation_swap_requests_list = list(mongo.db.shifts.aggregate([
        {"$match": {"$and": [
            {"_id": {"$in": rotation_swap_requests_ids}},
            {"drugstoreId": {"$ne": drugstore_id}}
        ]}},
        {"$project": {
            "_id": 0,
            "shiftId": {
                "$toString": "$_id"
            },
            "drugstoreId": 1,
            "from": 1,
            "to": 1
        }}
    ]))

    users_accepted_offers = list(mongo.db.swaps.aggregate([
        {"$match": {
            "accept": {"$in": users_shifts_ids}}},
        {"$project": {
            "_id": 0,
            "shiftId": 1,
            "accept": 1
        }},
        {"$unwind": "$accept"},
        {"$match": {
            "accept": {"$in": users_shifts_ids}}}
        ]))

    if len(users_accepted_offers) > 0:
        flash("Some of your offers were accepted! Please confirm the swap.")

    total_hours = 0
    for shift in users_shifts_list:
        total_hours += duration_to_readable(shift)

    return render_template("user.html",
                           yesterday_stamp=yesterday_stamp,
                           current_user=current_user,
                           users_shifts_list=users_shifts_list,
                           rotation_swaps_list=rotation_swaps_list,
                           rotation_swap_requests_list=rotation_swap_requests_list,
                           users_accepted_offers=users_accepted_offers,
                           total_hours=total_hours)
