import requests
from fastapi import FastAPI
from app.config import (
    BASEROW_TABLE_MAPPING,
    BASEROW_API,
    BASEROW_TOKEN,
    ZOTERO_API
)
app = FastAPI()

URL = "{}{}/?user_field_names=true"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/zotero/")
async def fetch_zotero_item(q: str):
    if len(q) < 3:
        return {
            "data": "please type at least three letters"
        }
    else:
        url = f"{ZOTERO_API}?q={q}"
        print(url)
        r = requests.get(url)
        data = r.json()
        return {
            "data": data
        }


@app.get("/baserow/{entity_type}")
async def fetch_entitey(entity_type: str, q: str):
    table_id = BASEROW_TABLE_MAPPING[entity_type]['table_id']
    query_field = BASEROW_TABLE_MAPPING[entity_type]['ac_query_field_id']
    try:
        lookup_type = BASEROW_TABLE_MAPPING[entity_type]['ac_lookup_type']
    except KeyError:
        lookup_type = "contains"

    if len(q) < 3:
        return {
            "data": "please type at least three letters"
        }
    else:
        url = URL.format(BASEROW_API, table_id)
        url = f"{url}&filter__{query_field}__{lookup_type}={q}"
        print(url)
        r = requests.get(
            url,
            headers={
                "Authorization": f"Token {BASEROW_TOKEN}"
            }
        )
        data = r.json()
        return {
            "table_id": url,
            "data": data
        }
