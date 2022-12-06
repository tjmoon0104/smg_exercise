# SMG GM Data Team - Data Engineer Python API Exercise

Python API Exercise

[![Checks](https://github.com/tjmoon0104/smg_exercise/actions/workflows/checks.yml/badge.svg?branch=main)](https://github.com/tjmoon0104/smg_exercise/actions/workflows/checks.yml)

## Description

This is a simple REST API containing two endpoints. This API allows you to get a sentence with the encrypted version of
it (with rot13), but also add new sentences in the existing store.

## Getting Started

### Assumptions

1. All the data in the storage has valid type (id: int, text: str)
2. All the data in the storage are unique (Already checked there are no duplicates)
3. If id exists in the storage it will return 409 conflict error

### File Description

* **main.py**: FastAPI GET & POST request
* **models.py**: Schema of Sentence & SentenceWithCypher
* **service.py**: Connector to Bigquery
* **test_main.py**: Testing API
* **utils.py**: rot13 encryption

### Local Setup

* place service account credentials from Google to app/credentials.json

### Executing program

```
docker-compose up
```

### Lint & Test

```
docker-compose run --rm app  sh -c "flake8"
docker-compose run --rm app  sh -c "pytest"
```

## CI/CD

This project is setup with Github actions with Google Workload Identity
Federation. ([Link](https://cloud.google.com/blog/products/identity-security/enabling-keyless-authentication-from-github-actions))

Separate docker-compose-github.yml is used for Github actions CI/CD.

```
command to run if program contains helper info
```

## Deployed URL to Cloud Run

https://smg-exercise-46o4qcp6xq-oa.a.run.app/sentences/1
