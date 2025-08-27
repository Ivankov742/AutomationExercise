import allure
import pytest
from tests.ui.pages.place_order_page import PlaceOrderPage
from tests.utils.logger import setup_logger

logger = setup_logger(__name__)

@pytest.mark.ui
@pytest.mark.order_flow
@allure.suite("UI Tests")
@allure.title("Place Order: Login before Checkout")
def test_place_order_login_before_checkout(page, config):
    base_url = config["base_url"]
    user = config["valid_user"]
    payment = config["payment"]

    place = PlaceOrderPage(page, base_url)

    with allure.step("Open homepage and login"):
        place.open_homepage()
        place.login(user["email"], user["password"])
        place.should_be_logged_in()
        logger.info("Logged in successfully")

    with allure.step("Add product and proceed to checkout"):
        place.add_product_to_cart()
        place.proceed_to_checkout()
        place.should_be_on_checkout(base_url)
        logger.info("On checkout page")

    with allure.step("Fill order message and go to payment"):
        place.fill_order_message_and_go_to_payment()

    with allure.step("Fill payment details and submit"):
        place.fill_payment_details_and_submit(payment)

    with allure.step("Verify order success"):
        place.should_see_success_message()
        logger.info("Order confirmed")
