
import functools
from flask import session, flash, redirect

def authenticated_route(view):
    """
        Wrapper for routes that require user to be logged in, as indicated by presence of "current_user" in the session.
        Prevents unauthenticated access.
        See also: https://flask.palletsprojects.com/en/2.0.x/tutorial/views/#require-authentication-in-other-views
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get("current_user"):
            #print("CURRENT USER:", session["current_user"])
            return view(**kwargs)
        else:
            print("UNAUTHENTICATED...")
            flash("Unauthenticated. Please login!", "warning")
            return redirect("/login")
    return wrapped_view
