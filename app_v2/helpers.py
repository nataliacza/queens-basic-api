from uuid import UUID

from fastapi.encoders import jsonable_encoder

from config import settings
from db.database import queens_db


def is_unique_name(fraze: str, given_data: list[dict[str, str]]) -> bool:
    """ Checks if field 'name' is unique across list. """
    for value in given_data:
        if fraze == value.get("name"):
            return False
    return True


def is_unique_name_update(fraze: str, given_data: list[dict[str, str]], update_id: str) -> bool:
    """ Checks if field 'name' is unique across list. Additional check for PUT requires id/key. """
    for value in given_data:
        if fraze == value.get("name"):
            if update_id == value.get("key"):
                return True
            return False
    return True


def is_assigned(search_id: UUID) -> bool:
    """ Checks whether city id is assigned to queen hometown or residence. """
    fetch_queens = queens_db.fetch().items
    for queen in fetch_queens:
        check_hometown = queen.get("hometown")
        check_residence = queen.get("residence")

        if check_hometown:
            if check_hometown.get("key") == search_id:
                return True

        if check_residence:
            if check_residence.get("key") == search_id:
                return True
    return False


def delete_tag_from_queens_db(category_key: str) -> None:
    """ When tag is deleted, it's reflected in queen db (like cascade delete). """
    encode_tag_key = jsonable_encoder(category_key)
    queens = queens_db.fetch().items
    for queen in queens:
        queen_tags = queen["tags"]
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("key") == encode_tag_key:
                del queen_tags[i]
                queens_db.update(updates={"tags": queen_tags},
                                 key=queen.get("key"),
                                 expire_at=settings.db_item_expire_at)


def update_tag_name_in_queens_db(category_key: str, update_name: str) -> None:
    """ When tag is updated, it's reflected in queen db. """
    encode_tag_key = jsonable_encoder(category_key)
    queens = queens_db.fetch().items
    for queen in queens:
        queen_tags = queen["tags"]
        for i, tag in enumerate(queen.get("tags")):
            if tag.get("key") == encode_tag_key:
                queen_tags[i]["name"] = update_name
                queens_db.update(updates={"tags": queen_tags},
                                 key=queen.get("key"),
                                 expire_at=settings.db_item_expire_at)


def update_city_in_queens_db(city_key: str, updated_data: dict) -> None:
    """ When city is updated, it's reflected in queen db. """
    encode_tag_key = jsonable_encoder(city_key)
    queens = queens_db.fetch().items
    for queen in queens:
        get_hometown = queen.get("hometown")
        get_residence = queen.get("residence")

        if get_hometown is not None:
            if get_hometown["key"] == encode_tag_key:
                get_hometown.update(updated_data)
                queens_db.update(updates={"hometown": get_hometown},
                                 key=queen.get("key"),
                                 expire_at=settings.db_item_expire_at)

        if get_residence is not None:
            if get_residence["key"] == encode_tag_key:
                get_residence.update(updated_data)
                queens_db.update(updates={"residence": get_residence},
                                 key=queen.get("key"),
                                 expire_at=settings.db_item_expire_at)
