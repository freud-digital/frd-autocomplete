import os

BASEROW_TOKEN = os.environ.get('BASEROW_TOKEN')

BASEROW_TABLE_MAPPING = {
    "keyword": {
        "table_id": "63650",
        "ac_query_field_id": "374368"
    },
    "person": {
        "table_id": "63642",
        "ac_query_field_id": "374327",
        "ac_lookup_type": "contains"
    },
    "place": {
        "table_id": "63334",
        "ac_query_field_id": "372296"
    },
    "org": {
        "table_id": "66452",
        "ac_query_field_id": "392881"
    },
    "dream": {
        "table_id": "63783",
        "ac_query_field_id": "375420"
    }
}

BASEROW_API = "https://api.baserow.io/api/database/rows/table/"
