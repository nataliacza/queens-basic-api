
def is_unique_name(fraze: str, given_data: list[dict[str, str]]) -> bool:
    """ Checks if field 'name' is unique across list. """
    for value in given_data:
        if fraze == value.get("name"):
            return False
    return True
