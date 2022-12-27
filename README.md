# GWU Course Catalogue Scraper (Python)

Gives you a CSV file of courses in a given subject, based on your filter criteria.


## Prerequisites

  + Python
  + Git
  + [Chromedriver](https://github.com/prof-rossetti/intro-to-python/blob/main/notes/clis/chromedriver.md)


## Setup

### Development Environment Setup

Setup a virtual environment:

```sh
conda create -n courses-env python=3.10
conda activate courses-env
```

Install packages:

```sh
pip install -r requirements.txt
```

Create ".env" file and set environment variables:

```sh
HEADLESS_MODE=true

# Google Login
GOOGLE_OAUTH_CLIENT_ID="______.apps.googleusercontent.com"
GOOGLE_OAUTH_CLIENT_SECRET="______"
```

### Google API Setup

Obtain credentials for accessing Google APIs. Visit the [Google Developer Console](https://console.developers.google.com/cloud-resource-manager). Create a new project, or select an existing one.

Enable the "Google Sheets API". Also enable the "Google Drive API".

From the Credentials page, click to "Create Credentials", specifically an "OAuth Client Id". Give it a name and set its redirect URL to "http://localhost:5000/login/callback". After the client is created, note the `GOOGLE_OAUTH_CLIENT_ID` and `GOOGLE_OAUTH_CLIENT_SECRET`, and set them as environment variables.

Click to "Configure Consent Screen".

From the Credentials page, click to "Create Credentials", specifically an "Service Account". Give it a name. Click on the service account link, and from the "Keys" tab, "Create new Key" specifically a "JSON" key. Download the resulting JSON file into the root directory of this repo as "google-credentials.json".

Then from the root directory of this repo, set the credentials as an environment variable:

```sh
export GOOGLE_API_CREDENTIALS="$(< google-credentials.json)"
# verify:
echo $GOOGLE_API_CREDENTIALS
```

## Usage

### Version 1 (Deprecated)

Browse the course catalogue for a give subject, and download a CSV file of the course listings:

```sh
python -m app.browser

# TERM_ID="202203" SUBJECT_ID="CSCI" python -m app.browser
```

> NOTE: this creates a new subdirectory in the "exports" dir corresponding with the subject name, and downloads the files there (e.g. "exports/CSCI/courses.csv")

After doing this for all interested subjects, compile a single file of all courses:

```sh
python -m app.compiler
```

### Version 2

This newer version stores the data in memory, and also leverages threading to speed up the process:

```sh
python -m app.multisubject

# HEADLESS_MODE=true TERM_ID="202203" SUBJECT_IDS="CSCI, EMSE" python -m app.multisubject
```

## Web App

Put the app in headless mode via `HEADLESS_MODE=true` in the ".env" file.

Run local webserver (then visit localhost:5000):

```sh
#FLASK_APP=web_app flask run

# flask --app web_app run --debug

flask --app web_app run --debugger
```

## Testing

Install test dependencies:

```sh
pip install -r requirements-test.txt
```

Run tests:

```sh
pytest

# APP_ENV="CI" pytest
```
