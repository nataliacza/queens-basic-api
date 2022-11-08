import uuid
from typing import Tuple

from app.db_memory import queen_db


def is_unique(search: str,
              db: dict,
              in_key: str = "name") -> bool:
    for value in db.values():
        if search == value.get(in_key):
            return False
    return True


def is_assigned(search_id: str,
                db: dict = queen_db,
                in_keys: Tuple[str] = ("hometown", "residence", "city_id")) -> bool:
    for value in db.values():
        check_hometown = value.get(in_keys[0]).get(in_keys[2])
        check_residence = value.get(in_keys[1]).get(in_keys[2])
        if search_id == check_hometown or search_id == check_residence:
            return True
    return False


def generate_new_uuid() -> str:
    new_id = str(uuid.uuid4())
    return new_id


def delete_tag_from_queens(category_id: str, db: dict = queen_db) -> None:
    for queen in db.values():
        for i, tag in enumerate(queen.get("tags")):
            if category_id in tag["category_id"]:
                del queen["tags"][i]

def update_tag_name_in_queens(category_id: str, update_name: str, db: dict = queen_db) -> None:
    for queen in db.values():
        for i, tag in enumerate(queen.get("tags")):
            if category_id in tag["category_id"]:
                queen["tags"][i]["name"] = update_name
                print(queen["tags"][i]["name"])
