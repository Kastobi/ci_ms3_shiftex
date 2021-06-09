from shiftex import create_app

app = create_app()

if __name__ == "__main__":
    app.run()

# todo: debug mode ! switch to gunicorn for submission!
