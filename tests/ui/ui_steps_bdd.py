import allure
import pytest
from pytest_bdd import scenarios, given, when, then
from tests.ui.pages.place_order_page import PlaceOrderPage

pytestmark = pytest.mark.ui
scenarios("../features/ui_tests.feature")

@pytest.fixture
def context():
    class Ctx:
        place_order: PlaceOrderPage | None = None
    return Ctx()

@given("I open the home page")
def open_home(page, config, context):
    base_url = config["base_url"]
    context.place_order = PlaceOrderPage(page, base_url)
    with allure.step("Open homepage"):
        context.place_order.open_homepage()

@given("I login with valid credentials")
def login_valid(context, config):
    user = config["valid_user"]
    with allure.step("Login with valid credentials"):
        context.place_order.login(user["email"], user["password"])  # type: ignore
        context.place_order.should_be_logged_in()  # type: ignore

@given("I add a product to the cart")
def add_product(context):
    with allure.step("Add product to cart"):
        context.place_order.add_product_to_cart()  # type: ignore

@given("I proceed to checkout")
def go_checkout(context, config):
    with allure.step("Proceed to checkout"):
        context.place_order.proceed_to_checkout()  # type: ignore
        context.place_order.should_be_on_checkout(config["base_url"])  # type: ignore

@given("I fill order message")
def fill_message(context):
    with allure.step("Fill order message & go to payment"):
        context.place_order.fill_order_message_and_go_to_payment()  # type: ignore

@when("I place the order")
def place_order(context, config):
    with allure.step("Fill payment details & submit"):
        context.place_order.fill_payment_details_and_submit(config["payment"])  # type: ignore

@then("the order should be confirmed")
def order_confirmed(context):
    with allure.step("Verify order success"):
        context.place_order.should_see_success_message()  # type: ignore
