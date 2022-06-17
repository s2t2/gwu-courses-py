# GWU Course Catalogue Scraper (Python)

Gives you a CSV file of courses in a given subject, based on your filter criteria.


## Prerequisites

  + Python
  + Git
  + [Chromedriver](https://github.com/prof-rossetti/intro-to-python/blob/main/notes/clis/chromedriver.md)

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

## Usage

Instructions TBD


```sh
python -m app.browser
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
