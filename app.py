import os

<<<<<<< Updated upstream
from flask import Flask
=======
from flask import Flask, render_template
>>>>>>> Stashed changes

if os.path.exists("env.py"):
    import env

app = Flask(__name__)


@app.route("/")
def index():
<<<<<<< Updated upstream
    return "Hello shiftex"
=======
    return render_template("index.html")
>>>>>>> Stashed changes


if __name__ == "__main__":
    app.run(
        debug=True)
# todo: debug mode !
