# frd-autocomplete

A fastapi proxy to query several different APIs and unify their response through a single API interface


## install & develop

* clone the repo
* create a virtual environment `virtualenv env`
* activate it `source env/bin/activate`
* update pip `pip install -U pip`
* install needed packages `pip install -r requirements.txt`

## run

`uvicorn app.main:app --reload`

## docker

### build & run

* `docker build -t frd-ac .`
* `docker run -d --name frd-ac -p 80:80 --env-file .env_secret frd-ac`

or just run `./build_and_run.sh`