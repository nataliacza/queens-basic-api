
import unittest
import uuid
from typing import Union, Any
from uuid import UUID

from app.helpers import (is_unique_name, is_assigned, delete_tag_from_queens_db, update_tag_name_in_queens_db,
                         update_city_in_queens_db, able_to_add_to_db)
from app.db_memory import category_db, city_db, queen_db
from schemas import City, Category, Queen


class TestIsUniqueValidator(unittest.TestCase):

    def test_when_name_exists_in_city_db_returns_false(self):
        # Arrange
        new_object = City(name="City123", region="test", country="test")
        city_db[new_object.city_id] = new_object.dict()
        # Act
        result = is_unique_name("City123", city_db)
        # Assert
        assert result is False
        # Clean
        del city_db[new_object.city_id]

    def test_when_name_does_not_exist_in_city_db_returns_true(self):
        # Arrange
        new_object = City(name="City123", region="test", country="test")
        city_db[new_object.city_id] = new_object.dict()
        # Act
        result = is_unique_name("City456", city_db)
        # Assert
        assert result is True
        # Clean
        del city_db[new_object.city_id]

    def test_when_id_and_name_match_to_the_same_item_returns_true(self):
        # Arrange
        new_object = City(name="City123", region="test", country="test")
        city_db[new_object.city_id] = new_object.dict()
        # Act
        result = is_unique_name("City123", city_db, new_object.city_id, "city_id")
        # Assert
        assert result is True
        # Clean
        del city_db[new_object.city_id]

    def test_when_id_and_name_does_not_match_to_the_same_item_returns_false(self):
        # Arrange
        new_object = City(name="City123", region="test", country="test")
        city_db[new_object.city_id] = new_object.dict()
        # Act
        result = is_unique_name("City123", city_db, uuid.uuid4(), "city_id")
        # Assert
        assert result is False
        # Clean
        del city_db[new_object.city_id]

    def test_when_name_exists_in_category_db_returns_false(self):
        # Arrange
        new_object = Category(name="cat123")
        category_db[new_object.category_id] = new_object.dict()
        # Act
        result = is_unique_name("cat123", category_db)
        # Assert
        assert result is False
        # Clean
        del category_db[new_object.category_id]

    def test_when_name_does_not_exist_in_category_db_returns_true(self):
        # Arrange
        new_object = Category(name="cat123")
        category_db[new_object.category_id] = new_object.dict()
        # Act
        result = is_unique_name("cat456", category_db)
        # Assert
        assert result is True
        # Clean
        del category_db[new_object.category_id]


class TestIsAssignedValidator(unittest.TestCase):

    def test_when_city_is_assigned_to_queen_hometown_returns_true(self):
        # Arrange
        new_city = City(name="City123", region="test", country="test")
        new_queen = Queen(nickname="TestNick", hometown=new_city)
        queen_db[new_queen.queen_id] = new_queen.dict()
        # Act
        result = is_assigned(new_city.city_id)
        # Assert
        assert result is True
        # Clean
        del queen_db[new_queen.queen_id]

    def test_when_city_is_assigned_to_queen_residence_returns_true(self):
        # Arrange
        new_city = City(name="City123", region="test", country="test")
        new_queen = Queen(nickname="TestNick", residence=new_city)
        queen_db[new_queen.queen_id] = new_queen.dict()
        # Act
        result = is_assigned(new_city.city_id)
        # Assert
        assert result is True
        # Clean
        del queen_db[new_queen.queen_id]

    def test_when_city_is_assigned_to_queen_residence_and_hometown_returns_true(self):
        # Arrange
        new_city = City(name="City123", region="test", country="test")
        new_queen = Queen(nickname="TestNick", residence=new_city, hometown=new_city)
        queen_db[new_queen.queen_id] = new_queen.dict()
        # Act
        result = is_assigned(new_city.city_id)
        # Assert
        assert result is True
        # Clean
        del queen_db[new_queen.queen_id]

    def test_when_city_is_not_assigned_to_queen_returns_false(self):
        # Arrange
        new_city = City(name="City123", region="test", country="test")
        # Act
        result = is_assigned(new_city.city_id)
        # Assert
        assert result is False


class TestDeleteCategoryFromQueenTags(unittest.TestCase):

    def test_when_category_is_assigned_to_queen_tags_its_deleted_queen_tags(self):
        # Arrange
        new_category = Category(name="cat123")
        new_queen = Queen(nickname="TestNick", tags=[new_category])
        queen_db[new_queen.queen_id] = new_queen.dict()
        # Act
        delete_tag_from_queens_db(new_category.category_id)
        # Assert
        get_queen = queen_db.get(new_queen.queen_id)
        assert len(get_queen["tags"]) == 0
        # Clean
        del queen_db[new_queen.queen_id]


class TestUpdateTagsInQueensDb(unittest.TestCase):

    def test_on_tag_update_its_updated_in_all_queens(self):
        # Arrange
        new_category = Category(name="cat123")
        new_queen = Queen(nickname="TestNick", tags=[new_category])
        new_queen2 = Queen(nickname="TestNick2", tags=[new_category])
        queen_db[new_queen.queen_id] = new_queen.dict()
        queen_db[new_queen2.queen_id] = new_queen2.dict()
        # Act
        update_tag_name_in_queens_db(new_category.category_id, "new_cat_name")
        # Assert
        get_queen_tags = queen_db.get(new_queen.queen_id)["tags"]
        get_queen2_tags = queen_db.get(new_queen2.queen_id)["tags"]
        assert get_queen_tags[0].get("name") == "new_cat_name"
        assert get_queen2_tags[0].get("name") == "new_cat_name"
        # Clean
        del queen_db[new_queen.queen_id]
        del queen_db[new_queen2.queen_id]


class TestUpdateCityInQueensDb(unittest.TestCase):

    def test_on_city_update_its_updated_in_queen_db(self):
        # Arrange
        new_city = City(name="City123", region="test", country="test")
        new_queen = Queen(nickname="TestNick", hometown=new_city, residence=new_city)
        queen_db[new_queen.queen_id] = new_queen.dict()
        # Act
        update_city_data = City(name="NewData", region="NewData", country="NewData").dict()
        update_city_in_queens_db(new_city.city_id, update_city_data)
        # Assert
        get_queen_hometown = queen_db.get(new_queen.queen_id)["hometown"]
        get_queen_residence = queen_db.get(new_queen.queen_id)["residence"]
        assert get_queen_hometown == update_city_data
        assert get_queen_residence == update_city_data
        # Clean
        del queen_db[new_queen.queen_id]


class TestDatabaseLimit(unittest.TestCase):

    def test_when_citi_db_got_19_elements_returns_true(self):
        # Arrange
        while len(city_db) != 19:
            city_db[uuid.uuid4()] = {}
        # Act
        result = able_to_add_to_db(city_db)
        assert result is True

    def test_when_citi_db_got_20_elements_returns_false(self):
        # Arrange
        while len(city_db) != 20:
            city_db[uuid.uuid4()] = {}
        # Act
        result = able_to_add_to_db(city_db)
        assert result is False
