# this is the "web_app/routes/search_routes.py" file...

from flask import Blueprint, request, render_template, flash

from app.browser import TERM_ID

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search/form")
def search_form():
    print("SEARCH FORM...")
    return render_template("search_form.html")

@search_routes.route("/search", methods=["GET", "POST"])
def search():
    print("COURSE SEARCH...")
    if request.method == "POST":
        request_data = dict(request.form)
    else:
        request_data = dict(request.args)
    print("REQUEST DATA:", request_data)

    try:
        term_id = request_data.get("term_id") or TERM_ID # app.config["DEFAULT_TERM"]
        subjects_csv = request_data.get("subject_ids") or ""
        subject_ids = subjects_csv
        courses = []

        message="Found X matching courses. Download should start shortly. Enjoy."
        flash(message, "success")
        return render_template("search_results.html", message=message)
    except Exception as err:
        print("OOPS", err)
        flash(f"OOPS, {err}. Please check your inputs and try again.", "danger")
        return redirect("/")
