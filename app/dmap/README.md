



# Degree Map

We need to programmatically parse the content of a student dashboard page, to find their GPA. There are a number of different GPA, including overall, in-major, in-major honors, special programs, etc. Ideally we will parse as much info as possible, however as a minimum viable product, we will grab the in-major honors GPA (because this is the GPA the department is interested in).

After downloading a student dashboard page from Degree Map as single source HTML file, we obtain a resulting .MHTML file. We save to the "test/mock_dmap" directory as "dashboard-`N`.mhtml".

These files are used during the automated testing process to quickly develop the page parsing capabilities (without the stakeholder needing to be there, logged in).

## Redaction Process

Since we value student privacy, it would not be responsible to upload the original files to GitHub.

Initially we searched for the single instance of the student's first and last name, and their GWID, and manually replaced those. We also replaced / redacted the admin's name in the top navbar.

However for some students, their page contents contained some potential personally-identifiable information (PII), such as a very specific conbination of major and niche minor, as well as their entire history of courses taken, as well as information about approvals from specific advisors.

So since right now we only need their top-level GPA information, to value the privacy of these students, we will redact the entire table body for all the tables on the page. Unfortunately this requires a time-consuming programmatic or manual process.

### Redacting TBODY

We tried an automated approach to redacting the TBODY, and it is easy to do, but when writing the content back to file, the content loses its styling, so it's harder to look at as a human.

~~So instead we are using a manual approach to redacting the content. We copy the unredacted file to "`filename`-redacted.mhtml". Then [using](https://stackoverflow.com/a/67065698/670433) the "Quick and Simple Text Selection" extension in VS Code, we redact everything inbetween `<tbody>` and `</tbody>`. JK that's not working.~~

For now we will keep the files ignored. Will skip the tests on CI.

## Setup

Obtain a list of GWID and save as CSV file "", where the header column name is "".

## Usage

Login to Degree Map as department admin, and visit all students pages, and export the result to CSV file (exports/_____.csv)

```sh
python -m app.dmap.honors_scraper
```

## Testing

```sh
pytest test/dmap/
```
