# this is the "web_app/routes/search_routes.py" file...

from flask import Blueprint, request, render_template, flash, redirect, Response
from pandas import DataFrame

from app.browser import TERM_ID
from app.multisubject import MultiSubjectBrowser

search_routes = Blueprint("search_routes", __name__)

#@search_routes.route("/search/form")
#def search_form():
#    print("SEARCH FORM...")
#    return render_template("search_form.html")

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
        subject_ids = request_data.get("subject_ids")

        browser = MultiSubjectBrowser(term_id=term_id, subject_ids=subject_ids)
        courses = browser.fetch_all_courses()
        courses_df = DataFrame(courses)

        message=f"Found {len(courses_df)} matching courses. Download should start shortly. Enjoy."
        flash(message, "success")
        #return render_template("search_results.html", message=message, courses=courses)

        # trigger CSV file download
        # ... https://stackoverflow.com/a/61508751/670433
        # ... https://tedboy.github.io/flask/generated/generated/flask.Response.html
        # ... The Location response-header field is used to redirect the recipient to a location other than the Request-URI for completion of the request or identification of a new resource.
        return Response(courses_df.to_csv(),
            mimetype="text/csv",
            headers={
                "Content-disposition": "attachment; filename=colonial_courses.csv",
                #"Location":"/?success" # redirect, to trigger flash NOPE JK
            }
        )
    except Exception as err:
        print("OOPS", err)
        flash(f"OOPS, {err}. Please check your inputs and try again.", "danger")
        return redirect("/")
