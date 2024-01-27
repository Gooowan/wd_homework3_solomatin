def get_item_by_id(id, list):
    return next(filter(lambda x: x['id'] == id, list), None)
