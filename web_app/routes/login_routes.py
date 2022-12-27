
from flask import Blueprint, render_template, flash, redirect, current_app, url_for, session, request
from datetime import datetime

from web_app.routes.auth import authenticated_route

login_routes = Blueprint("login_routes", __name__)

#
# LOGIN WITH GOOGLE ROUTES
#

@login_routes.route("/login")
def login():
    #return redirect("/login/form")
    return render_template("login.html")

#@login_routes.route("/login/form")
#def login_form():
#    print("LOGIN FORM...")
#    return render_template("login_form.html")

@login_routes.route("/login/redirect", methods=["GET", "POST"])
def login_redirect():
    print("LOGIN REDIRECT...")
    oauth = current_app.config["OAUTH"]
    redirect_uri = url_for("login_routes.login_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@login_routes.route("/login/callback")
def login_callback():
    print("LOGIN CALLBACK...")

    oauth = current_app.config["OAUTH"]

    try:
        # user info (below) needs this to be invoked, even if not directly using the token
        # avoids... authlib.integrations.base_client.errors.MissingTokenError: missing_token
        token = oauth.google.authorize_access_token()
        print("TOKEN:", list(token.keys()))
        #> {
        #>     'access_token': '___.___-___-___-___-___-___',
        #>     'expires_at': 1621201708,
        #>     'expires_in': 3599,
        #>     'id_token': '___.___.___-___-___-___-___',
        #>     'refresh_token': "____",
        #>     'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid',
        #>     'token_type': 'Bearer'
        #> }

        user_info = oauth.google.userinfo() #> <class 'authlib.oidc.core.claims.UserInfo'>
        user_info = dict(user_info)
        print("GOOGLE USER INFO:", list(user_info.keys()))

        #user = User.query.filter_by(email=user_info["email"]).first() or User(email=user_info["email"])
        #user.email_verified = user_info["email_verified"] #> True
        #user.last_name = user_info["family_name"] #> 'Student'
        #user.first_name = user_info["given_name"] #> 'Sammy S'
        #user.full_name = user_info["name"] #> 'Sammy S Student'
        #user.locale = user_info["locale"] #> "en"
        #user.picture = user_info["picture"] #> 'https://lh3.googleusercontent.com/a-/___=___-___'
        #user.sub = user_info["sub"] #> 'abc123def456789'
        #user.provider_id = "google"
        #now = datetime.now()
        #user.last_login_at=now
        #user.last_refresh_at=now

        # store user info in the session:
        session["current_user"] = user_info
        # store the token for later maybe?
        session["bearer_token"] = token

        flash(f"Login success. Welcome, {user_info['given_name']}!", "success")
        return redirect("/")

    except Exception as err:
        print("OOPS", err)
        flash(f"OOPS, login error.", "danger")
        return redirect("/login")


@login_routes.route("/logout")
def logout():
    print("LOGOUT...")
    #session.clear() # FYI: this clears the flash as well
    # so be more surgical:
    for k in ["current_user", "bearer_token"]:
        try:
            del session[k]
        except KeyError:
            pass
    # although we probably want to clear all non flash related keys
    # and refactor with the session clearing of courses
    return redirect("/login")


#
# PROFILE ROUTES
#

@login_routes.route("/user/profile")
@authenticated_route
def profile():
    print("PROFILE...")
    current_user = session.get("current_user")
    #user = User.query.filter_by(email=current_user["email"]).first()
    return render_template("user_profile.html", current_user=current_user) #, user=user)
