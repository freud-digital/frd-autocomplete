[![flake8 Lint](https://github.com/freud-digital/frd-autocomplete/actions/workflows/lint.yml/badge.svg)](https://github.com/freud-digital/frd-autocomplete/actions/workflows/lint.yml)
[![Test](https://github.com/freud-digital/frd-autocomplete/actions/workflows/test.yml/badge.svg)](https://github.com/freud-digital/frd-autocomplete/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/freud-digital/frd-autocomplete/branch/main/graph/badge.svg?token=miLq3rRrcq)](https://codecov.io/gh/freud-digital/frd-autocomplete)

# frd-autocomplete

A fastapi proxy to query several different APIs and unify their response through a single API interface


## install & develop

* clone the repo
* create a virtual environment `virtualenv env`
* activate it `source env/bin/activate`
* update pip `pip install -U pip`
* install needed packages `pip install -r requirements.txt`

## run

`uvicorn app.main:app --reload` (or simply `./startserver.sh`)

## test 

`./run_tests.sh`

## docker

### build & run

* `docker build -t frd-ac .`
* `docker run -d --name frd-ac -p 80:80 --env-file .env_secret frd-ac`

or just run `./build_and_run.sh`

### use published image

docker run -d --name frd-ac-officical -p 80:80 --env-file env.secret ghcr.io/freud-digital/frd-autocomplete:main