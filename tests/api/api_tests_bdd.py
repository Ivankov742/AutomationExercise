import requests
import allure
from pytest_bdd import scenarios, when, then, parsers

# Load feature file relative to this file
scenarios("../features/api_tests.feature")

BASE_URL = "https://automationexercise.com/api"

@when(parsers.parse("I try to login with email '{email}' and password '{password}'"))
def login_response(email, password, request):
    with allure.step(f"Send POST request to {BASE_URL}/verifyLogin"):
        response = requests.post(f"{BASE_URL}/verifyLogin", data={
            "email": email,
            "password": password
        })
        request._login_response = response

@then("the login response code should be 400 or 404")
def verify_login_response_code(request):
    response = request._login_response
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    response_body = response.json()
    assert response_body.get("responseCode") in [400, 404, 405], f"Unexpected responseCode: {response_body}"

@when(parsers.parse("I search for product '{search_product}'"))
def search_response(search_product, request):
    with allure.step(f"Send POST request to {BASE_URL}/searchProduct"):
        response = requests.post(f"{BASE_URL}/searchProduct", data={
            "search_product": search_product
        })
        request._search_response = response

@then("the search response code should be 200")
def verify_search_response_code(request):
    response = request._search_response
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    response_body = response.json()
    assert response_body.get("responseCode") == 200, f"Unexpected responseCode: {response_body}"
    assert "products" in response_body, "Expected 'products' in response"
