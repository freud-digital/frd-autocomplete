import os

BASEROW_TOKEN = os.environ.get('BASEROW_TOKEN')

BASEROW_TABLE_MAPPING = {
    "keyword": {
        "table_id": "1470",
        "ac_query_field_id": "field_12412"
    },
    "person": {
        "table_id": "1474",
        "ac_query_field_id": "field_12428",
        "ac_lookup_type": "contains"
    },
    "place": {
        "table_id": "1468",
        "ac_query_field_id": "field_12396"
    },
    "org": {
        "table_id": "1476",
        "ac_query_field_id": "field_12447"
    },
    "dream": {
        "table_id": "1475",
        "ac_query_field_id": "field_12443"
    },
    "profession": {
        "table_id": "1473",
        "ac_query_field_id": "field_12424"
    },
    "label": {
        "table_id": "1469",
        "ac_query_field_id": "field_12404"
    }
}

BASEROW_API = "https://baserow.acdh-dev.oeaw.ac.at/api/database/rows/table/"

ZOTERO_GROUP_ID = "4690432"
ZOTERO_API = f"https://api.zotero.org/groups/{ZOTERO_GROUP_ID}/items"

MINIMAL_CHARS = 3
MINIMAL_CHARS_ERROR = f"please type at least {MINIMAL_CHARS} letters"
