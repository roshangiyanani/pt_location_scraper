# Physical Therapy Location Scraper

A tool for scraping the website of physical therapy websites to get their locations.

## Documentation

### Supported Physical Therapy Companies

* Athletica
* ATI
* US Physical Therapy (USPh)

### (Hopefully soon to be) supported physical therapy websites

* Select Physical Therapy
* Novacare
* Pivot Physical Therapy
* Professional PT
* Upstream Rehabilitation
* Fyzical
* CORA Health Services

### Output format

The code outputs the data into individual csv files, which can then be opened in excel or your favorite text editor.

### To run

To run the program:

~~~~bash
pipenv run python ptls
~~~~

## Installation

Installation requires pipenv, which you can install by running:

~~~~bash
pip install pipenv
~~~~

To install dependencies:

~~~~bash
pipenv sync
pipenv run pip install -e ./  # pointing to the project root directory
~~~~