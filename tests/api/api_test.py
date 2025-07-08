import pytest
import allure
from playwright.sync_api import sync_playwright

LOGIN_URL = "https://automationexercise.com/api/verifyLogin"
SEARCH_URL = "https://automationexercise.com/api/searchProduct"

@allure.suite("API Tests")
@allure.title("Verify login with invalid credentials")
def test_login_invalid_api():
    with sync_playwright() as p:
        context = p.request.new_context()
        response = context.post(LOGIN_URL, multipart={
            "email": "invalid@example.com",
            "password": "wrongpassword"
        })
        assert response.status == 200
        assert response.json()["responseCode"] in [400, 404]

@allure.suite("API Tests")
@allure.title("Search product using keyword")
def test_search_product_api():
    with sync_playwright() as p:
        context = p.request.new_context()
        response = context.post(SEARCH_URL, multipart={
            "search_product": "tshirt"
        })
        assert response.status == 200
        assert response.json()["responseCode"] in [200, 400]
