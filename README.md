# Data discrepancy checker

## Feature

- API Endpoint `/compare`: A user can provide a PDF and a company name data is extracted from the PDF via
  the external service and compared to the data stored on file a summary of the
  data is returned, containing all fields from both sources, noting which fields
  did not match.

## Setup using Poetry

The easiest way to set up the repository is to use `python-poetry`. The lock file
was generated using version `1.8.3`

1. Ensure `poetry` is installed
2. Run `make install`

## Run using poetry

Run `make dev`

## Tests

Run `make test`

## Setup without Poetry

Alternatively it's possible to `pip install` directly using the
`pyproject.toml` or `requirements.txt`.
