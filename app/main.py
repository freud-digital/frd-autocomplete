import requests
from typing import Union
from fastapi import FastAPI, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from app.config import (
    BASEROW_TABLE_MAPPING,
    BASEROW_API,
    BASEROW_TOKEN,
    ZOTERO_API,
    MINIMAL_CHARS,
    MINIMAL_CHARS_ERROR
)
from app.utils import populate_baserow_response, populate_zotero_response


app = FastAPI()

URL = "{}{}/?user_field_names=true"


@app.get("/")
@cache(expire=60 * 60)
async def root(request: Request):
    endpoints = [
        {
            "entity-type": x,
            "endpoint": f"{request.url._url}{x}"
        } for x in BASEROW_TABLE_MAPPING
    ] + [
        {
            "entity-type": "bibl",
            "endpoint": f"{request.url._url}bibl"
        },
    ]

    return {
        "message": "Hello World",
        "docs": f"{request.url._url}docs",
        "endpoints": endpoints,
    }


@app.get("/{entity_type}")
@cache(expire=60 * 60)
async def fetch_entitiy(
    entity_type: str,
    q: str,
    format: Union[str, None] = "teicompleter"
):
    if len(q) < MINIMAL_CHARS:
        return {
            "data": MINIMAL_CHARS_ERROR
        }
    else:
        if entity_type == 'bibl':
            url = f"{ZOTERO_API}?q={q}"
            r = requests.get(url)
            data = r.json()

            result = populate_zotero_response(data, format=format)
            return result
        else:
            table_id = BASEROW_TABLE_MAPPING[entity_type]['table_id']
            query_field = BASEROW_TABLE_MAPPING[entity_type]['ac_query_field_id']
            try:
                lookup_type = BASEROW_TABLE_MAPPING[entity_type]['ac_lookup_type']
            except KeyError:
                lookup_type = "contains"
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
            result = populate_baserow_response(data, format=format)
            return result


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())
