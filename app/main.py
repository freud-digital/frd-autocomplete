import requests
from typing import Union
from fastapi import FastAPI, Request
from app.config import (
    BASEROW_TABLE_MAPPING,
    BASEROW_API,
    BASEROW_TOKEN,
    ZOTERO_API
)
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
async def fetch_entitey(
    entity_type: str,
    q: str,
    format: Union[str, None] = "teicompleter"
):
    if len(q) < 3:
        return {
            "data": "please type at least three letters"
        }
    else:
        if entity_type == 'bibl':
            url = f"{ZOTERO_API}?q={q}"
            print(url)
            r = requests.get(url)
            data = r.json()

            if format == 'teicompleter':
                result = {
                    "tc:suggestion": []
                }
                for x in data:
                    item_data = x['data']
                    item_title = item_data.get('title', 'no title provided')
                    item_place = item_data.get('place', 'no place provided')
                    item_date = item_data.get('date', 'no date provided')
                    item = {
                        "tc:value": x['key'],
                        "tc:description": f"{item_title}, {item_place}, {item_date}"
                    }
                    result['tc:suggestion'].append(item)

                return result

            elif format == 'select2':
                result = {
                    "results": [],
                }
                for x in data['data']:
                    item_data = x['data']
                    item_title = item_data.get('title', 'no title provided')
                    item_place = item_data.get('place', 'no place provided')
                    item_date = item_data.get('date', 'no date provided')
                    item = {
                        "id": x['key'],
                        "text": f"{item_title}, {item_place}, {item_date}"
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
                        "tc:value": x['frd_id'],
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
                        "id": x['frd_id'],
                        "text": x['name']
                    }
                    result['results'].append(item)

                return result

            elif format == 'original':

                return {
                    "table_id": url,
                    "data": data
                }
