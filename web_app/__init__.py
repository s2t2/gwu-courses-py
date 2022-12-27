import os
from dotenv import load_dotenv

from flask import Flask
from flask_session import Session
from authlib.integrations.flask_client import OAuth

from web_app.routes.home_routes import home_routes
from web_app.routes.login_routes import login_routes
from web_app.routes.search_routes import search_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")

GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")


def create_app(test_config=None):

    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY

    # https://flask-session.readthedocs.io/en/latest/
    # server-side sessions because data is too large to store in client side session:
    # ... avoid "UserWarning: The 'session' cookie is too large" h/t: https://stackoverflow.com/a/53554226/670433
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    # this produces lots of session files, which might bloat the server, so consider
    #app.config["SESSION_PERMANENT"] = True
    #app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30) # False
    Session(app)

    # ROUTES

    app.register_blueprint(home_routes)
    app.register_blueprint(login_routes)
    app.register_blueprint(search_routes)

    # GOOGLE LOGIN

    oauth = OAuth(app)
    oauth_scopes = "openid email profile" # +  " " + " ".join(GCAL_SCOPES)
    oauth.register(
        name="google",
        client_id=GOOGLE_OAUTH_CLIENT_ID,
        client_secret=GOOGLE_OAUTH_CLIENT_SECRET,
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": oauth_scopes},
        authorize_params={"access_type": "offline"} # give us the refresh token! see: https://stackoverflow.com/questions/62293888/obtaining-and-storing-refresh-token-using-authlib-with-flask
    ) # now you can also access via: oauth.google (the name specified during registration)
    app.config["OAUTH"] = oauth

    return app


#if __name__ == "__main__":
#    my_app = create_app()
#    my_app.run(debug=True)
