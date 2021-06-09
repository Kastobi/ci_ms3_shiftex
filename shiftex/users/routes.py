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
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))

    form = LoginForm()

    if form.validate_on_submit():
        check_user = mongo.db.users.find_one({"email": form.email.data})
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
    logout_user()
    flash(f"Logout successful!")
    return redirect(url_for("main.index"))


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.user"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        User.register_user(form.first_name.data,
                           form.last_name.data,
                           form.email.data,
                           form.drugstore_id.data,
                           hashed_password)
        flash(f"Registration complete for {form.first_name.data} {form.last_name.data}.")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@login_required
@users.route("/user")
def user():
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
                           current_user=current_user,
                           users_shifts_list=users_shifts_list,
                           rotation_swaps_list=rotation_swaps_list,
                           rotation_swap_requests_list=rotation_swap_requests_list,
                           users_accepted_offers=users_accepted_offers,
                           yesterday_stamp=yesterday_stamp,
                           total_hours=total_hours)


@login_required
@users.route("/admin")
def admin():
    overview = {"count_shifts": int(mongo.db.shifts.count_documents({})),
                "count_pharmacies": len(mongo.db.shifts.distinct("drugstoreId")),
                "count_rotation_plans": len(mongo.db.shifts.distinct("planId")),
                "count_rotations": len(mongo.db.shifts.distinct("digitsId"))
                }
    return render_template("admin.html", overview=overview)
