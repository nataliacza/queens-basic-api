from uuid import UUID

from app.db_memory import queen_db


def is_unique(search: str, db: dict, in_key: str = "name",
              given_id: UUID = None, pk_name: str = None) -> bool:
    """ Checks if field is unique across given db. For PUT method additional
    check for matching id and name was required. """
    for value in db.values():
        if given_id:
            if value.get(pk_name) == given_id and value.get(in_key) == search:
                return True
        if search == value.get(in_key):
            return False
    return True


def is_assigned(search_id: UUID) -> bool:
    """ Checks if city id is assigned to queen db. """
    for value in queen_db.values():
        check_hometown = value.get("hometown")
        check_residence = value.get("residence")

        if check_hometown:
            if check_hometown.get("city_id") == search_id:
                return True

        if check_residence:
            if check_residence.get("city_id") == search_id:
                return True
    return False


def delete_tag_from_queens_db(category_id: UUID | str) -> None:
    """ When tag is deleted, it's reflected in queen db (like cascade delete). """
    for queen in queen_db.values():
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("category_id") == category_id:
                del queen["tags"][i]


def update_tag_name_in_queens_db(category_id: UUID, update_name: str) -> None:
    """ When tag is updated, it's reflected in queen db. """
    for queen in queen_db.values():
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("category_id") == category_id:
                queen["tags"][i]["name"] = update_name


def update_city_in_queens_db(city_id: UUID, new_data_cleaned: dict) -> None:
    """ When city is updated, it's reflected in queen db. """
    for queen in queen_db.values():
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
