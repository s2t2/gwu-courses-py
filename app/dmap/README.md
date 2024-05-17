



# Degree Map

We need to programmatically parse the content of a student dashboard page, to find their GPA. There are a number of different GPA, including overall, in-major, in-major honors, special programs, etc. Ideally we will parse as much info as possible, however as a minimum viable product, we will grab the in-major honors GPA ("Departmental/Special Honors") because this is the one the department is interested in.


## For Students

For a student user, with access to only their own information.

Run the scraper:

```sh
python -m app.dmap.student
```

This will export the student's degree requirement info to "exports/dmap/student_dashboard.csv".

## For Department Advisors

For a department advisor with access to student search capabilities.

Setup: Obtain a CSV file of student GWID identifiers in the department, and save it as "data/dmap/`DEPT`/student_ids.csv", where `DEPT` is the department abbreviation (e.g. "PSC"). The expected header column name is "gwid". See an example file at "data/dmap/example_student_ids.csv".

Run the scraper:

```sh
python -m app.dmap.advisor

DEPT="PSC" python -m app.dmap.advisor
```

This will export the degree requirement info for all students to "exports/dmap/`DEPT`/student_dashboards.csv".

## Testing

Running tests:

```sh
pytest test/dmap/
```

### Mock Dashboards

After downloading a student dashboard page from Degree Map as single source HTML file, we obtain a resulting .MHTML file. We save to the "test/mock_dmap" directory as "dashboard-`N`.mhtml".

These files are used during the automated testing process to quickly develop the page parsing capabilities (without the advisor needing to be there, logged in).

#### Redaction Process

For each mock student dashboard, we took the following redaction measures:

  + We redacted the student's first name, last name, and GWID.
  + We redacted the admin's name in the top navbar.
  + We changed / obscured the GPA values.
  + We changed / obscured some of the majors and minors.

Because there is some additional potential PII in the files that would need to be further redacted (such as unique sequence of courses taken, as well as specific advisor information), for now we will keep the original files ignored from version control (see ".gitignore"). And we will skip the corresponding tests on CI.
