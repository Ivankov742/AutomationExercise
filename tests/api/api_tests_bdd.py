import json
import allure
import pytest
from pytest_bdd import scenarios, when, then, parsers
from tests.api.client import ApiClient

pytestmark = pytest.mark.api
scenarios("../features/api_tests.feature")

@pytest.fixture(scope="session")
def client(config):
    return ApiClient(config["base_url"])

@pytest.fixture
def api_ctx():
    class Ctx:
        last_response = None
    return Ctx()

@when(parsers.parse('I POST "{endpoint}" with form data:'))
def post_with_form_data(client: ApiClient, api_ctx, endpoint, doc_string):
    data = json.loads(doc_string)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    with allure.step(f'POST /api/{endpoint}'):
        resp = client._post(f"/api/{endpoint}", data=data, headers=headers)
        api_ctx.last_response = resp

@when(parsers.parse('I GET "{endpoint}"'))
def get_endpoint(client: ApiClient, api_ctx, endpoint):
    with allure.step(f'GET /api/{endpoint}'):
        resp = client._get(f"/api/{endpoint}")
        api_ctx.last_response = resp

@then(parsers.parse("the API response status should be {code:d}"))
def assert_status(api_ctx, code: int):
    assert api_ctx.last_response is not None, "No response captured"
    assert api_ctx.last_response.status_code == code

@then(parsers.parse('the JSON field "{field}" should equal {expected}'))
def assert_json_equals(api_ctx, field: str, expected: str):
    body = api_ctx.last_response.json()
    try:
        exp_val = int(expected)
    except ValueError:
        exp_val = expected.strip('"').strip("'")
    assert field in body, f'Missing field "{field}" in response'
    assert body[field] == exp_val, f'Expected {field}={exp_val}, got {body[field]}'

@then(parsers.parse('the JSON field "{field}" should contain "{snippet}"'))
def assert_json_contains(api_ctx, field: str, snippet: str):
    body = api_ctx.last_response.json()
    assert field in body, f'Missing field "{field}" in response'
    assert snippet.lower() in str(body[field]).lower(), f'"{snippet}" not in {field}: {body[field]}'

@then(parsers.parse('the JSON should have key "{key}"'))
def assert_json_has_key(api_ctx, key: str):
    body = api_ctx.last_response.json()
    assert key in body, f'Missing key "{key}" in response'

@then(parsers.parse('the JSON field "{field}" should be one of {codes}'))
def assert_json_in_codes(api_ctx, field: str, codes: str):
    body = api_ctx.last_response.json()
    assert field in body, f'Missing field "{field}" in response'
    allowed = []
    for part in codes.split(","):
        part = part.strip()
        if part:
            try:
                allowed.append(int(part))
            except ValueError:
                allowed.append(part.strip('"').strip("'"))
    assert body[field] in allowed, f'Expected {field} in {allowed}, got {body[field]}'
