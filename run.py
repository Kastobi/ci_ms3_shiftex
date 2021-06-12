"""
shiftex run.py
==============

Creates the app with create_app from shiftex.__init__.py file,
afterwards running it.

For Heroku deployment host and port have to be passed in to app.run()
"""

# pylint: disable=unused-import
# env.py is wrongly highlighted

import os

from shiftex import create_app

if os.path.exists("env.py"):
    import env


"""
to run specific configurations, pass an Config Object
further documentation in shiftex.__init__.py
"""
app = create_app()

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP"),
        port=os.getenv("PORT"))
