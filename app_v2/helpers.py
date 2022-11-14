from uuid import UUID

from database import queens_db


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
