def zotero_description(item_data: dict) -> dict:
    item_title = item_data.get('title', 'no title provided')
    item_place = item_data.get('place', 'no place provided')
    item_date = item_data.get('date', 'no date provided')
    item_id = f"#frd_bibl_{item_data['key']}"
    item_description = f"{item_title}, {item_place}, {item_date}"
    return {
        "id": item_id,
        "value": item_description
    }
