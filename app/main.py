import requests
from typing import Union
from fastapi import FastAPI, Request
from app.config import (
    BASEROW_TABLE_MAPPING,
    BASEROW_API,
    BASEROW_TOKEN,
    ZOTERO_API,
    MINIMAL_CHARS,
    MINIMAL_CHARS_ERROR
)
from app.utils import zotero_description


app = FastAPI()

URL = "{}{}/?user_field_names=true"


@app.get("/")
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
            print(url)
            r = requests.get(url)
            data = r.json()
            print(data)
            if format == 'teicompleter':
                result = {
                    "tc:suggestion": []
                }
                for x in data:
                    item_data = zotero_description(x['data'])
                    item = {
                        "tc:value": item_data['id'],
                        "tc:description": item_data['value']
                    }
                    result['tc:suggestion'].append(item)
                return result

            elif format == 'select2':
                result = {
                    "results": [],
                }
                for x in data:
                    item_data = zotero_description(x['data'])
                    item = {
                        "id": item_data['id'],
                        "text": item_data['value']
                    }
                    result['results'].append(item)
                return result

            elif format == 'original':
                return data
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

            if format == 'teicompleter':
                result = {
                    "tc:suggestion": []
                }
                for x in data['results']:
                    item = {
                        "tc:value": f"#{x['frd_id']}",
                        "tc:description": x['name']
                    }
                    result['tc:suggestion'].append(item)

                return result

            elif format == 'select2':
                result = {
                    "results": [],
                }
                for x in data['results']:
                    item = {
                        "id": f"#{x['frd_id']}",
                        "text": x['name']
                    }
                    result['results'].append(item)

                return result

            elif format == 'original':

                return {
                    "table_id": url,
                    "data": data
                }
