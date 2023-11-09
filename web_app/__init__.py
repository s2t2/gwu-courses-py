import os
from dotenv import load_dotenv
from flask import Flask
from flask_session import Session

from web_app.routes.home_routes import home_routes
from web_app.routes.search_routes import search_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")
GA_TRACKER_ID = os.getenv("GA_TRACKER_ID", default="G-OOPS")


def create_app(test_config=None):

    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["GA_TRACKER_ID"] = GA_TRACKER_ID

    # https://flask-session.readthedocs.io/en/latest/
    # server-side sessions because data is too large to store in client side session:
    # ... avoid "UserWarning: The 'session' cookie is too large" h/t: https://stackoverflow.com/a/53554226/670433
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    # this produces lots of session files, which might bloat the server, so consider
    #app.config["SESSION_PERMANENT"] = True
    #app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # False
    Session(app)

    app.register_blueprint(home_routes)
    app.register_blueprint(search_routes)

    return app


#if __name__ == "__main__":
#    my_app = create_app()
#    my_app.run(debug=True)
