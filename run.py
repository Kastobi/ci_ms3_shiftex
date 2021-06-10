import os

from shiftex import create_app

if os.path.exists("env.py"):
    import env

app = create_app()

# todo: debug mode ! switch to gunicorn for submission!
if __name__ == "__main__":
    app.run()
