# frd-autocomplete

A fast-api proxy to query several different APIs and unify their response through a single API interface


## install & develop

* clone the repo
* create a virtual environment `virtualenv env`
* activate it `source env/bin/activate`
* update pip `pip install -U pip`
* install needed packages `pip install -r requirements.txt`

## run

`uvicorn main:app --reload`