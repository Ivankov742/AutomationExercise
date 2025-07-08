import pytest
import allure
from pytest_bdd import scenarios, given, when, then
from tests.ui.pages.place_order_page import PlaceOrderPage

scenarios("../features/ui_tests.feature")

EMAIL = "qa_testuser_01@example.com"
PASSWORD = "123456"

@pytest.fixture
def context():
    class Context:
        pass
    return Context()

@given("I open the home page")
def open_home_page(page, context):
    context.place_order = PlaceOrderPage(page)
    context.place_order.open_homepage()

@given("I login with valid credentials")
def login_with_valid_credentials(context):
    context.place_order.login(EMAIL, PASSWORD)
    assert context.place_order.verify_logged_in()

@given("I add a product to the cart")
def add_product_to_cart(context):
    context.place_order.add_product_to_cart()

@given("I proceed to checkout")
def proceed_to_checkout(context):
    context.place_order.proceed_to_checkout()

@given("I fill payment details")
def fill_payment_details(context):
    context.place_order.fill_order_message_and_place_order()

@when("I place the order")
def place_order(context):
    context.place_order.fill_payment_details_and_submit()

@then("the order should be confirmed")
def verify_order_confirmation(context):
    success_message = context.place_order.verify_order_success()
    assert "Congratulations! Your order has been confirmed!" in success_message
