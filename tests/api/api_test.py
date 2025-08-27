import allure
import pytest
from tests.api.client import ApiClient

pytestmark = pytest.mark.api

@allure.suite("API Tests")
class TestApi:
    @pytest.fixture(scope="class")
    def client(self, config):
        return ApiClient(config["base_url"])

    @allure.title("Login with invalid credentials returns 404 in body")
    def test_login_invalid_api(self, client, config):
        inv = config["invalid_user"]
        r = client.verify_login(inv["email"], inv["password"])
        assert r.status_code == 200
        body = r.json()
        assert body["responseCode"] == 404
        assert "user not found" in body["message"].lower()

    @allure.title("Search product by keyword returns products")
    def test_search_product_api(self, client, config):
        r = client.search_product(config["search"]["query_positive"])
        assert r.status_code == 200
        body = r.json()
        assert body["responseCode"] == 200
        assert "products" in body

    @allure.title("GET method is not supported (or returns parameter missing)")
    def test_search_product_with_get_method(self, client):
        r = client.search_product_get()
        assert r.status_code == 200
        body = r.json()
        assert body["responseCode"] in (400, 405)
        assert any(k in body["message"].lower() for k in ["method is not supported", "missing"])
