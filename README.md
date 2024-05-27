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

## Test with swagger UI

1. Run `make dev`
2. Open `http://127.0.0.1:8000/docs`
3. Open `/compare` api endpoint and click on `Try it out` button
   <img src="/screenshots/1.png" />
   <img src="/screenshots/2.png" />
4. Test with differents `company_name` and `file` values
   <img src="/screenshots/3.png" />
   <img src="/screenshots/4.png" />
   <img src="/screenshots/5.png" />

## Tests

Run `make test`

## Setup without Poetry

Alternatively it's possible to `pip install` directly using the
`pyproject.toml` or `requirements.txt`.
