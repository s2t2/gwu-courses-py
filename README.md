# GWU Course Catalogue Scraper (Python)

Gives you a CSV file of courses in a given subject, based on your filter criteria.

[![Maintainability](https://api.codeclimate.com/v1/badges/331f73a256080399c798/maintainability)](https://codeclimate.com/github/s2t2/gwu-courses-py/maintainability)

![Tests](https://github.com/s2t2/gwu-courses-py/actions/workflows/python-app.yml/badge.svg)

## Prerequisites

  + Python
  + Git
  + [Chromedriver](https://github.com/prof-rossetti/intro-to-python/blob/main/notes/clis/chromedriver.md)

### Chromedriver

Installing Chromedriver (and Chrome Binary) on Mac:

```sh
# chromedriver:
brew install chromedriver
brew upgrade chromedriver

# chrome binary:
brew install google-chrome
brew upgrade google-chrome
```

> NOTE: on Mac you need to also mark chromedriver as a trusted app from the Security and Privacy settings
>
> NOTE: if you see errors like "This version of ChromeDriver only supports Chrome version 119 Current browser version is 123.0.6312.58", then make sure to update / upgrade chromedriver, and also update the Security Privacy settings to use the new version

## Setup

### Virtual Environment

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
# this is the ".env" file...

FLASK_APP="web_app"
HEADLESS_MODE=true

# Mac:
CHROME_BINARY_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

## Usage

### Command Line App

#### Course Search Version 1 (Deprecated)

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

#### Course Search Version 2

This newer version stores the data in memory, and also leverages threading to speed up the process:

```sh
python -m app.multisubject

# HEADLESS_MODE=true TERM_ID="202303" SUBJECT_IDS="CSCI, EMSE" python -m app.multisubject
```

### Web App

Put the app in headless mode via `HEADLESS_MODE=true` in the ".env" file.

Run local webserver (then visit localhost:5000):

```sh
#FLASK_APP=web_app flask run

# flask --app web_app run --debug

flask --app web_app run --debugger
```






## Testing

Run tests:

```sh
pytest
# APP_ENV="CI" pytest
```

## [Deploying](/DEPLOYING.md)
