



# Degree Map

We need to programmatically parse the content of a student dashboard page, to find their GPA. There are a number of different GPA, including overall, in-major, in-major honors, special programs, etc. Ideally we will parse as much info as possible, however as a minimum viable product, we will grab the in-major honors GPA (because this is the GPA the department is interested in).


## Setup

### Students List

Obtain a CSV file of student identifiers, and save it as "data/dmap/`DEPT`/student_ids.csv", where `DEPT` is the department abbreviation (e.g. "PSC").

The expected header column name is "gwid". See an example file at "data/dmap/example_student_ids.csv".

## Usage

Honors scraper will output a CSV file of results to "exports/dmap/`DEPT`/honors_records.csv", where `DEPT` is the department abbreviation (e.g. "PSC").

```sh
python -m app.dmap.honors_scraper
```

## Testing

Running tests:

```sh
pytest test/dmap/
```

### Mock Dashboards

After downloading a student dashboard page from Degree Map as single source HTML file, we obtain a resulting .MHTML file. We save to the "test/mock_dmap" directory as "dashboard-`N`.mhtml".

These files are used during the automated testing process to quickly develop the page parsing capabilities (without the stakeholder needing to be there, logged in).

#### Redaction Process

For each mock student dashboard, we took the following redaction measures:

  + We redacted the student's first name, last name, and GWID.
  + We redacted the admin's name in the top navbar.
  + We changed / obscured the GPA values.

Because there is some additional potential PII in the files that would need to be further redacted, for now we will keep the original files ignored. And we will skip the corresponding tests on CI.
