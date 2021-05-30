import os
import time
import datetime

from flask import Flask, render_template, url_for
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_restful import Api, Resource

from forms import LoginForm, RegistrationForm

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

api = Api(app)


class SwapQueriesAPI(Resource):
    def get(self, input_id):
        swaps_plan_cursor = list(mongo.db.swaps.find({"planId": int(input_id)}))
        if len(swaps_plan_cursor) == 0:
            return {"error": "Not Found"}, 404

        else:
            swaps_plan = []
            for document in swaps_plan_cursor:
                document.pop("_id")
                swaps_plan.append(document)
            return swaps_plan, 200

    def put(self, input_id):
        check_swaps = mongo.db.swaps.find_one({"shiftId": input_id})
        if check_swaps is not None:
            return {"error": "Already there"}, 409

        else:
            find_shift_cursor = mongo.db.shifts.find_one({"_id": ObjectId(input_id)})
            query_document = {
                "shiftId": input_id,
                "drugstoreId": find_shift_cursor["drugstoreId"],
                "planId": find_shift_cursor["planId"],
                "digitsId": find_shift_cursor["digitsId"],
                "offer": [],
                "reject": [],
                "accept": []
            }
            mongo.db.swaps.insert_one(query_document)
            return {"success": "Swap query posted"}, 201

    def delete(self, input_id):
        check_swaps = mongo.db.swaps.find_one({"shiftId": input_id})
        if check_swaps is None:
            return {"error": "Not Found"}, 404

        else:
            mongo.db.swaps.delete_one({"shiftId": input_id})
            return "", 204


api.add_resource(SwapQueriesAPI, "/api/swaps/<input_id>", endpoint="swap_queries")


@app.template_filter()
def timestamp_to_readable(timestamp):
    timestamp = timestamp // 1000
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt


@app.template_filter()
def duration_to_readable(shift):
    shift_start = timestamp_to_readable(shift["from"])
    shift_end = timestamp_to_readable(shift["to"])
    duration = shift_end - shift_start
    return duration.total_seconds() // 3600


@app.route("/")
def index():
    today_time = time.strftime("%A, %d %b %Y", time.localtime())
    now_unixtime = int(time.time()) * 1000
    today_duty_list = list(mongo.db.shifts.find(
        {"$and": [
            {"from": {"$lt": now_unixtime}},
            {"to": {"$gt": now_unixtime}}
        ]}))
    return render_template("index.html", today_duty_list=today_duty_list, today_time=today_time)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    return render_template("register.html", form=form)


@app.route("/user")
def user():
    user_id = 1664005
    shifts_list = list(mongo.db.shifts.find(
        {"drugstoreId": user_id}
    ))

    total_hours = 0
    for shift in shifts_list:
        total_hours += duration_to_readable(shift)

    return render_template("user.html", shifts_list=shifts_list, total_hours=total_hours)


@app.route("/admin")
def admin():
    overview = {"count_shifts": int(mongo.db.shifts.count_documents({})),
                "count_pharmacies": len(mongo.db.shifts.distinct("drugstoreId")),
                "count_rotation_plans": len(mongo.db.shifts.distinct("planId")),
                "count_rotations": len(mongo.db.shifts.distinct("digitsId"))
                }
    return render_template("admin.html", overview=overview)


if __name__ == "__main__":
    app.run(
        debug=True)
# todo: debug mode !
