from uuid import UUID
from typing import Tuple

from app.db_memory import queen_db


def is_unique(search: str, db: dict, in_key: str = "name",
              given_id: UUID = None, pk_name: str = None) -> bool:
    """ Function that checks if field is unique across db. For PUT method additional
    check for matching id and name is added. """
    for value in db.values():
        if given_id:
            if value.get(pk_name) == given_id and value.get(in_key) == search:
                return True
        if search == value.get(in_key):
            return False
    return True


def is_assigned(search_id: str, db: dict = queen_db,
                in_keys: Tuple[str] = ("hometown", "residence", "city_id")) -> bool:
    for value in db.values():
        check_hometown = value.get(in_keys[0]).get(in_keys[2])
        check_residence = value.get(in_keys[1]).get(in_keys[2])
        if search_id == check_hometown or search_id == check_residence:
            return True
    return False


def delete_tag_from_queens_db(category_id: UUID | str, db: dict = queen_db) -> None:
    for queen in db.values():
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("category_id") == category_id:
                del queen["tags"][i]


def update_tag_name_in_queens_db(category_id: UUID, update_name: str, db: dict = queen_db) -> None:
    for queen in db.values():
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("category_id") == category_id:
                queen["tags"][i]["name"] = update_name


def update_city_in_queens_db(city_id: UUID, new_data_cleaned: dict, db: dict = queen_db) -> None:
    for queen in db.values():
        get_hometown = queen.get("hometown")
        get_residence = queen.get("residence")

        if get_hometown is not None:
            if get_hometown["city_id"] == city_id:
                get_hometown.update(new_data_cleaned)

        if get_residence is not None:
            if get_residence["city_id"] == city_id:
                get_residence.update(new_data_cleaned)


def able_to_add_to_db(db: dict, limit: int = 20) -> bool:
    """ Checks the limit of in-memory data. Default limit is 20. """
    if len(db) >= limit:
        return False
    return True
