
def is_unique(search: str, db: dict, in_key: str = "name") -> bool:
    for value in db.values():
        if search == value.get(in_key):
            return False
    return True
