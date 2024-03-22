# this is the "web_app/routes/search_routes.py" file...

from flask import Blueprint, request, render_template, flash, redirect, Response, session
from pandas import DataFrame

#from app.browser import TERM_ID
from app.multisubject import MultiSubjectBrowser

search_routes = Blueprint("search_routes", __name__)

#@search_routes.route("/search/form")
#def search_form():
#    print("SEARCH FORM...")
#    return render_template("search_form.html")

def clear_session():
    # clearing the entire session will remove flash messages as well, so let's be more surgical
    for k in ["courses", "term_id", "subject_ids", "subject_ids_csv"]:
        try:
            del session[k]
        except KeyError:
            pass




@search_routes.route("/search", methods=["GET", "POST"])
def search():
    print("COURSE SEARCH...")
    if request.method == "POST":
        request_data = dict(request.form)
    else:
        request_data = dict(request.args)
    print("REQUEST DATA:", request_data)

    try:
        #term_id = request_data.get("term_id") or TERM_ID
        year = request_data.get("year") # "2024"
        semester_id = request_data.get("semester_id") # "01"
        term_id = f"{year}{semester_id}"

        subject_ids = request_data.get("subject_ids")

        browser = MultiSubjectBrowser(term_id=term_id, subject_ids=subject_ids)
        #courses = browser.fetch_all_courses()
        courses = browser.fetch_all_courses_threaded() # parallel processing to help avoid timeouts

        #message=f"Found {len(courses_df)} matching courses. Download should start shortly. Enjoy."
        #flash(message, "success")
        ##return render_template("search_results.html", message=message, courses=courses)
        #
        ## trigger CSV file download
        ## ... https://stackoverflow.com/a/61508751/670433
        ## ... https://tedboy.github.io/flask/generated/generated/flask.Response.html
        ## ... The Location response-header field is used to redirect the recipient to a location other than the Request-URI for completion of the request or identification of a new resource.
        #courses_df = DataFrame(courses)
        #return Response(courses_df.to_csv(),
        #    mimetype="text/csv",
        #    headers={
        #        "Content-disposition": "attachment; filename=colonial_courses.csv",
        #        #"Location":"/?success" # redirect, to trigger flash NOPE JK
        #    }
        #)

        clear_session()
        session["courses"] = courses
        session["subject_ids"] = sorted(browser.subject_ids)
        session["subject_ids_csv"] = ", ".join(session["subject_ids"])
        session["term_id"] = browser.term_id

        message=f"Found {len(courses)} matching courses across {len(browser.subject_ids)} subjects."
        flash(message, "success")
        #return render_template("search_results.html", message=message, courses=courses)
        return redirect("/search/results")
    except Exception as err:
        print("OOPS", err)
        flash(f"OOPS, {err}. Please check your inputs and try again.", "danger")
        return redirect("/")




@search_routes.route("/search/results")
def search_results():
    print("SEARCH RESULTS...")
    courses = session["courses"]
    return render_template("search_results.html", courses=courses)



@search_routes.route("/search/results/download")
def download_csv():
    print("DOWNLOAD COURSES...")

    courses = session["courses"]

    # trigger CSV file download
    # ... https://stackoverflow.com/a/61508751/670433
    # ... https://tedboy.github.io/flask/generated/generated/flask.Response.html
    # ... The Location response-header field is used to redirect the recipient to a location other than the Request-URI for completion of the request or identification of a new resource.
    print(len(courses))
    courses_df = DataFrame(courses)
    return Response(courses_df.to_csv(),
        mimetype="text/csv",
        headers={
            "Content-disposition": "attachment; filename=colonial_courses.csv",
            #"Location":"/?success" # redirect, to trigger flash NOPE JK
        }
    )



#@search_routes.route("/search/results/export")
#def export_google_sheets():
#    print("EXPORT COURSES...")
#
#    courses = session["courses"]
#
#    print("TODO")
