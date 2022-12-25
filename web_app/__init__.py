import os
from dotenv import load_dotenv
from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.search_routes import search_routes

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", default="super secret")

def create_app(test_config=None):

    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    #app.config["TERM_ID"] = TERM_ID

    app.register_blueprint(home_routes)
    app.register_blueprint(search_routes)

    return app


#if __name__ == "__main__":
#    my_app = create_app()
#    my_app.run(debug=True)
