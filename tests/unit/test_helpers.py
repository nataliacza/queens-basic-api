
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

