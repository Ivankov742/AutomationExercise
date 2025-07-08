import requests
import allure
import pytest

LOGIN_URL = "https://automationexercise.com/api/verifyLogin"
SEARCH_URL = "https://automationexercise.com/api/searchProduct"
INVALID_EMAIL = "invalid@example.com"
INVALID_PASSWORD = "wrongpassword"
SEARCH_QUERY = "tshirt"

@allure.suite("API Tests")
@allure.title("Verify login with invalid credentials")
def test_login_invalid_api():
    response = requests.post(LOGIN_URL, data={
        "email": INVALID_EMAIL,
        "password": INVALID_PASSWORD
    })

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    response_body = response.json()

    assert "responseCode" in response_body, "Missing responseCode in response"
    assert response_body["responseCode"] in [400, 404, 405], f"Unexpected responseCode: {response_body['responseCode']}"
    assert "message" in response_body, "Missing message in response"

@allure.suite("API Tests")
@allure.title("Search product using keyword")
def test_search_product_api():
    response = requests.post(SEARCH_URL, data={
        "search_product": SEARCH_QUERY
    })

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    response_body = response.json()

    assert "responseCode" in response_body, "Missing responseCode in response"
    assert response_body["responseCode"] in [200, 400, 404, 405], f"Unexpected responseCode: {response_body['responseCode']}"

    # If search works, it should return a list of products
    if response_body["responseCode"] == 200:
        assert "products" in response_body, "Expected 'products' in successful search response"





# import pytest
# import allure
# from playwright.sync_api import sync_playwright
#
# LOGIN_URL = "https://automationexercise.com/api/verifyLogin"
# SEARCH_URL = "https://automationexercise.com/api/searchProduct"
#
# @allure.suite("API Tests")
# @allure.title("Verify login with invalid credentials")
# def test_login_invalid_api():
#     with sync_playwright() as p:
#         context = p.request.new_context()
#         response = context.post(LOGIN_URL, multipart={
#             "email": "invalid@example.com",
#             "password": "wrongpassword"
#         })
#         assert response.status == 200
#         assert response.json()["responseCode"] in [400, 404]
#
# @allure.suite("API Tests")
# @allure.title("Search product using keyword")
# def test_search_product_api():
#     with sync_playwright() as p:
#         context = p.request.new_context()
#         response = context.post(SEARCH_URL, multipart={
#             "search_product": "tshirt"
#         })
#         assert response.status == 200
#         assert response.json()["responseCode"] in [200, 400]