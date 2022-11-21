""" Those tests are required to make sure 'relations' are properly assigned especially for all objects
in queen database. """

import unittest
from uuid import UUID

from db_memory import category_db, city_db, queen_db


class TestCityDatabase(unittest.TestCase):

    def test_city_db_got_2_items(self):
        result = len(city_db)
        assert result == 2

    def test_all_keys_are_UUID(self):
        get_keys = list(city_db.keys())
        result = list(set(isinstance(i, UUID) for i in get_keys))
        assert len(result) == 1
        assert result[0] is True

    def test_warszawa_in_db(self):
        result = city_db.get(UUID("eb195501-603e-46f4-b3f1-71f7de304a28"))
        assert result is not None
        assert isinstance(result["city_id"], UUID) is True
        assert result["city_id"] == UUID("eb195501-603e-46f4-b3f1-71f7de304a28")
        assert result["name"] == "Warszawa"
        assert result["region"] == "Mazowieckie"
        assert result["country"] == "Polska"

    def test_krakow_in_db(self):
        result = city_db.get(UUID("7ced7771-64ff-44e5-8a87-c0f4126a6328"))
        assert result is not None
        assert isinstance(result["city_id"], UUID) is True
        assert result["city_id"] == UUID("7ced7771-64ff-44e5-8a87-c0f4126a6328")
        assert result["name"] == "Kraków"
        assert result["region"] == "Małopolskie"
        assert result["country"] == "Polska"


class TestCategoryDatabase(unittest.TestCase):

    def test_category_db_got_4_items(self):
        result = len(category_db)
        assert result == 4

    def test_all_keys_are_UUID(self):
        get_keys = list(category_db.keys())
        result = list(set(isinstance(i, UUID) for i in get_keys))
        assert len(result) == 1
        assert result[0] is True

    def test_glam_in_db(self):
        result = category_db.get(UUID("8898ea70-2c02-4551-9658-691e3293c516"))
        assert result is not None
        assert isinstance(result["category_id"], UUID) is True
        assert result["category_id"] == UUID("8898ea70-2c02-4551-9658-691e3293c516")
        assert result["name"] == "glam"

    def test_makeup_in_db(self):
        result = category_db.get(UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2"))
        assert result is not None
        assert isinstance(result["category_id"], UUID) is True
        assert result["category_id"] == UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2")
        assert result["name"] == "makeup"

    def test_camp_in_db(self):
        result = category_db.get(UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35"))
        assert result is not None
        assert isinstance(result["category_id"], UUID) is True
        assert result["category_id"] == UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35")
        assert result["name"] == "camp"

    def test_wig_in_db(self):
        result = category_db.get(UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf"))
        assert result is not None
        assert isinstance(result["category_id"], UUID) is True
        assert result["category_id"] == UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf")
        assert result["name"] == "wig"


class TestQueenDatabase(unittest.TestCase):

    def test_queen_db_got_3_items(self):
        result = len(queen_db)
        assert result == 3

    def test_all_keys_are_UUID(self):
        get_keys = list(queen_db.keys())
        result = list(set(isinstance(i, UUID) for i in get_keys))
        assert len(result) == 1
        assert result[0] is True

    def test_hrabina_in_db(self):
        result = queen_db.get(UUID("d43ee99a-038e-4381-8b10-b014ff7253cd"))
        assert result is not None
        assert isinstance(result["queen_id"], UUID) is True
        assert result["queen_id"] == UUID("d43ee99a-038e-4381-8b10-b014ff7253cd")
        assert result["nickname"] == "Hrabina"

    def test_hrabina_got_2_tags(self):
        result = queen_db.get(UUID("d43ee99a-038e-4381-8b10-b014ff7253cd"))
        assert len(result["tags"]) == 2
        assert result["tags"][0].get("category_id") == UUID("f82466c4-4a4c-4a08-aaec-00667324e3bf")
        assert result["tags"][0].get("name") == "wig"
        assert result["tags"][1].get("category_id") == UUID("8898ea70-2c02-4551-9658-691e3293c516")
        assert result["tags"][1].get("name") == "glam"

    def test_misia_in_db(self):
        result = queen_db.get(UUID("6c9463b7-bf69-4f8d-87dd-f1aa10a27762"))
        assert result is not None
        assert isinstance(result["queen_id"], UUID) is True
        assert result["queen_id"] == UUID("6c9463b7-bf69-4f8d-87dd-f1aa10a27762")
        assert result["nickname"] == "Misia Joachim"

    def test_misia_got_2_tags(self):
        result = queen_db.get(UUID("6c9463b7-bf69-4f8d-87dd-f1aa10a27762"))
        assert len(result["tags"]) == 2
        assert result["tags"][0].get("category_id") == UUID("b11ab87c-b7d5-4dd9-a640-0bbe545abfe2")
        assert result["tags"][0].get("name") == "makeup"
        assert result["tags"][1].get("category_id") == UUID("8898ea70-2c02-4551-9658-691e3293c516")
        assert result["tags"][1].get("name") == "glam"

    def test_stara_in_db(self):
        result = queen_db.get(UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"))
        assert result is not None
        assert isinstance(result["queen_id"], UUID) is True
        assert result["queen_id"] == UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1")
        assert result["nickname"] == "Twoja Stara"

    def test_stara_got_1_tag(self):
        result = queen_db.get(UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"))
        assert len(result["tags"]) == 1
        assert result["tags"][0].get("category_id") == UUID("57940578-16f4-45ec-9ac4-ad2e45b11b35")
        assert result["tags"][0].get("name") == "camp"

    def test_stara_got_hometown_assigned(self):
        result = queen_db.get(UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"))
        assert result["hometown"] is not None
        assert result["hometown"].get("city_id") == UUID("eb195501-603e-46f4-b3f1-71f7de304a28")
        assert result["hometown"].get("name") == "Warszawa"

    def test_stara_got_residence_assigned(self):
        result = queen_db.get(UUID("30c9c75d-dd6c-47fa-b932-e5a5c3fc08c1"))
        assert result["residence"] is not None
        assert result["residence"].get("city_id") == UUID("eb195501-603e-46f4-b3f1-71f7de304a28")
        assert result["residence"].get("name") == "Warszawa"
