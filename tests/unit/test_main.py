import unittest
import uuid

from fastapi.encoders import jsonable_encoder
from starlette.testclient import TestClient

from main import app
from schemas import QueenSave, CategorySave, CitySave

test_client = TestClient(app)

class TestGetQueen(unittest.TestCase):

    def test_endpoint_response_200(self):
        response = test_client.get("/api/v1/queens/")
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


class TestGetOneQueen(unittest.TestCase):

    def test_when_id_exists_returns_200(self):
        queen_id = "6c9463b7-bf69-4f8d-87dd-f1aa10a27762"
        response = test_client.get(f"/api/v1/queens/{queen_id}")
        assert response.status_code == 200
        assert response.json().get("queen_id") == queen_id

    def test_when_id_does_not_exist_returns_404(self):
        queen_id = uuid.uuid4()
        response = test_client.get(f"/api/v1/queens/{queen_id}")
        assert response.status_code == 404

    def test_when_id_is_not_valid_uuid_returns_422(self):
        queen_id = "invalid-id-format"
        response = test_client.get(f"/api/v1/queens/{queen_id}")
        assert response.status_code == 422


class TestAddQueen(unittest.TestCase):

    def test_empty_body_provided_returns_422(self):
        response = test_client.post("/api/v1/queens/")
        assert response.status_code == 422

    def test_when_nickname_provided_returns_201(self):
        queen_data = QueenSave(nickname="Test Name")
        response = test_client.post("/api/v1/queens/", json=jsonable_encoder(queen_data))
        assert response.status_code == 201
        assert response.json().get("queen_id") is not None
        assert response.json().get("nickname") == "Test Name"

    def test_when_hometown_id_does_not_exist_returns_404(self):
        queen_data = QueenSave(nickname="Test Name", hometown=uuid.uuid4())
        response = test_client.post("/api/v1/queens/", json=jsonable_encoder(queen_data))
        assert response.status_code == 404

    def test_when_residence_id_does_not_exist_returns_404(self):
        queen_data = QueenSave(nickname="Test Name", residence=uuid.uuid4())
        response = test_client.post("/api/v1/queens/", json=jsonable_encoder(queen_data))
        assert response.status_code == 404

    def test_when_tag_id_does_not_exist_returns_404(self):
        queen_data = QueenSave(nickname="Test Name", tags=[uuid.uuid4()])
        response = test_client.post("/api/v1/queens/", json=jsonable_encoder(queen_data))
        assert response.status_code == 404


class TestUpdateQueen(unittest.TestCase):

    def test_when_id_not_exist_returns_404(self):
        queen_data = QueenSave(nickname="Test Name")
        response = test_client.put(f"/api/v1/queens/{uuid.uuid4()}", json=jsonable_encoder(queen_data))
        assert response.status_code == 404

    def test_when_hometown_id_does_not_exist_returns_404(self):
        queen_id = "d43ee99a-038e-4381-8b10-b014ff7253cd"
        update_data = QueenSave(nickname="Test Name", hometown=uuid.uuid4())
        response = test_client.put(f"/api/v1/queens/{queen_id}", json=jsonable_encoder(update_data))
        assert response.status_code == 404

    def test_when_residence_id_does_not_exist_returns_404(self):
        queen_id = "d43ee99a-038e-4381-8b10-b014ff7253cd"
        update_data = QueenSave(nickname="Test Name", residence=uuid.uuid4())
        response = test_client.put(f"/api/v1/queens/{queen_id}", json=jsonable_encoder(update_data))
        assert response.status_code == 404

    def test_when_tag_id_does_not_exist_returns_404(self):
        queen_id = "d43ee99a-038e-4381-8b10-b014ff7253cd"
        update_data = QueenSave(nickname="Test Name", tags=[uuid.uuid4()])
        response = test_client.put(f"/api/v1/queens/{queen_id}", json=jsonable_encoder(update_data))
        assert response.status_code == 404

    def test_when_valid_data_provided_returns_200(self):
        queen_id = "6c9463b7-bf69-4f8d-87dd-f1aa10a27762"
        update_data = QueenSave(nickname="Test Name",
                                hometown="eb195501-603e-46f4-b3f1-71f7de304a28",
                                residence="eb195501-603e-46f4-b3f1-71f7de304a28",
                                tags=["8898ea70-2c02-4551-9658-691e3293c516"])
        response = test_client.put(f"/api/v1/queens/{queen_id}", json=jsonable_encoder(update_data))
        assert response.status_code == 200
        assert response.json().get("queen_id") == queen_id
        assert response.json().get("hometown") is not None
        assert response.json().get("residence") is not None
        assert len(response.json().get("tags")) != 0


class TestDeleteQueen(unittest.TestCase):

    def test_when_id_not_exist_returns_404(self):
        response = test_client.delete(f"/api/v1/queens/{uuid.uuid4()}")
        assert response.status_code == 404

    def test_when_id_exists_returns_204(self):
        queen_id = "d43ee99a-038e-4381-8b10-b014ff7253cd"
        response = test_client.delete(f"/api/v1/queens/{queen_id}")
        assert response.status_code == 204


class TestGetCategories(unittest.TestCase):

    def test_endpoint_response_200(self):
        response = test_client.get("/api/v1/categories/")
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


class TestGetOneCategory(unittest.TestCase):

    def test_when_id_exists_returns_200(self):
        category_id = "8898ea70-2c02-4551-9658-691e3293c516"
        response = test_client.get(f"/api/v1/categories/{category_id}")
        assert response.status_code == 200
        assert response.json().get("category_id") == category_id

    def test_when_id_does_not_exist_returns_404(self):
        category_id = uuid.uuid4()
        response = test_client.get(f"/api/v1/categories/{category_id}")
        assert response.status_code == 404

    def test_when_id_is_not_valid_uuid_returns_422(self):
        category_id = "invalid-id-format"
        response = test_client.get(f"/api/v1/categories/{category_id}")
        assert response.status_code == 422


class TestAddCategory(unittest.TestCase):

    def test_empty_body_provided_returns_422(self):
        response = test_client.post("/api/v1/categories/")
        assert response.status_code == 422

    def test_when_data_provided_returns_201(self):
        category_data = CategorySave(name="Test")
        response = test_client.post("/api/v1/categories/", json=jsonable_encoder(category_data))
        assert response.status_code == 201
        assert response.json().get("category_id") is not None
        assert response.json().get("name") == "test"

    def test_when_category_name_already_exist_returns_400(self):
        category_data = CategorySave(name="glam")
        response = test_client.post("/api/v1/categories/", json=jsonable_encoder(category_data))
        assert response.status_code == 400

    def test_when_category_name_is_unique_returns_201(self):
        category_data = CategorySave(name="newone")
        response = test_client.post("/api/v1/categories/", json=jsonable_encoder(category_data))
        assert response.status_code == 201


class TestDeleteCategory(unittest.TestCase):

    def test_when_id_exists_returns_204(self):
        category_id = "f82466c4-4a4c-4a08-aaec-00667324e3bf"
        response = test_client.delete(f"/api/v1/categories/{category_id}")
        assert response.status_code == 204

    def test_when_id_does_not_exist_returns_404(self):
        category_id = uuid.uuid4()
        response = test_client.delete(f"/api/v1/categories/{category_id}")
        assert response.status_code == 404


class TestUpdateCategory(unittest.TestCase):

    def test_name_not_provided_returns_422(self):
        category_id = "8898ea70-2c02-4551-9658-691e3293c516"
        response = test_client.put(f"/api/v1/categories/{category_id}")
        assert response.status_code == 422

    def test_when_id_does_not_exist_returns_404(self):
        category_id = uuid.uuid4()
        category_data = CategorySave(name="test")
        response = test_client.put(f"/api/v1/categories/{category_id}", json=jsonable_encoder(category_data))
        assert response.status_code == 404

    def test_valid_data_provided_returns_200(self):
        category_id = "57940578-16f4-45ec-9ac4-ad2e45b11b35"
        category_data = CategorySave(name="SomeData")
        response = test_client.put(f"/api/v1/categories/{category_id}", json=jsonable_encoder(category_data))
        assert response.status_code == 200
        assert response.json().get("name") == "somedata"


class TestGetCity(unittest.TestCase):

    def test_endpoint_response_200(self):
        response = test_client.get("/api/v1/cities/")
        assert response.status_code == 200
        assert isinstance(response.json(), list) is True


class TestGetOneCity(unittest.TestCase):

    def test_when_id_exists_returns_200(self):
        city_id = "eb195501-603e-46f4-b3f1-71f7de304a28"
        response = test_client.get(f"/api/v1/cities/{city_id}")
        assert response.status_code == 200
        assert response.json().get("city_id") == city_id

    def test_when_id_does_not_exist_returns_404(self):
        city_id = uuid.uuid4()
        response = test_client.get(f"/api/v1/cities/{city_id}")
        assert response.status_code == 404

    def test_when_id_is_not_valid_uuid_returns_422(self):
        city_id = "invalid-id-format"
        response = test_client.get(f"/api/v1/cities/{city_id}")
        assert response.status_code == 422


class TestAddCity(unittest.TestCase):

    def test_empty_body_provided_returns_422(self):
        response = test_client.post("/api/v1/cities/")
        assert response.status_code == 422

    def test_when_valid_data_provided_returns_201(self):
        city_data = CitySave(name="Test123", region="Test123", country="Test123")
        response = test_client.post("/api/v1/cities/", json=jsonable_encoder(city_data))
        assert response.status_code == 201
        assert response.json().get("city_id") is not None
        assert response.json().get("name") == "Test123"
        assert response.json().get("region") == "Test123"
        assert response.json().get("country") == "Test123"

    def test_when_city_name_already_exist_returns_400(self):
        city_data = CitySave(name="Warszawa", region="Test123", country="Test123")
        response = test_client.post("/api/v1/cities/", json=jsonable_encoder(city_data))
        assert response.status_code == 400


class TestDeleteCity(unittest.TestCase):

    def test_when_id_exists_returns_204(self):
        city_id = "7ced7771-64ff-44e5-8a87-c0f4126a6328"
        response = test_client.delete(f"/api/v1/cities/{city_id}")
        assert response.status_code == 204

    def test_when_id_does_not_exist_returns_404(self):
        city_id = uuid.uuid4()
        response = test_client.delete(f"/api/v1/cities/{city_id}")
        assert response.status_code == 404

    def test_when_city_is_assigned_to_queen_returns_409(self):
        city_id = "eb195501-603e-46f4-b3f1-71f7de304a28"
        response = test_client.delete(f"/api/v1/cities/{city_id}")
        assert response.status_code == 409


class TestUpdateCity(unittest.TestCase):

    def test_when_mandatory_fields_not_provided_returns_422(self):
        city_id = "eb195501-603e-46f4-b3f1-71f7de304a28"
        response = test_client.put(f"/api/v1/cities/{city_id}")
        assert response.status_code == 422

    def test_when_id_does_not_exist_returns_404(self):
        city_id = uuid.uuid4()
        city_data = CitySave(name="TestXYZ", region="TestXYZ", country="TestXYZ")
        response = test_client.put(f"/api/v1/cities/{city_id}", json=jsonable_encoder(city_data))
        assert response.status_code == 404

    def test_valid_data_provided_returns_200(self):
        city_id = "eb195501-603e-46f4-b3f1-71f7de304a28"
        city_data = CitySave(name="Testname", region="Testname", country="Testname")
        response = test_client.put(f"/api/v1/cities/{city_id}", json=jsonable_encoder(city_data))
        assert response.status_code == 200
        assert response.json().get("city_id") == city_id
        assert response.json().get("name") == "Testname"
        assert response.json().get("region") == "Testname"
        assert response.json().get("country") == "Testname"
