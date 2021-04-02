import os

from flask import Flask

if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello shiftex"


if __name__ == "__main__":
    app.run(
        debug=True)
# todo: debug mode !
