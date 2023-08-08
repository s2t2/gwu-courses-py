# GWU Course Catalogue Scraper (Python)

Gives you a CSV file of courses in a given subject, based on your filter criteria.


## Prerequisites

  + Python
  + Git
  + [Chromedriver](https://github.com/prof-rossetti/intro-to-python/blob/main/notes/clis/chromedriver.md)

Installing Chromedriver on Mac:

```sh
#brew install chromedriver
#brew upgrade chromedriver
#brew install google-chrome
```

## Setup

Setup a virtual environment:

```sh
conda create -n courses-env python=3.10
conda activate courses-env
```

Install packages:

```sh
pip install -r requirements.txt
```

Configure environment variables in ".env" file:

```sh
# Mac:
CHROME_BINARY_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

## Usage

### Version 1

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
