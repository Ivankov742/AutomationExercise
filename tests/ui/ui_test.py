import pytest
import logging
from tests.ui.pages.place_order_page import PlaceOrderPage
from playwright.sync_api import expect

EMAIL = "qa_testuser_01@example.com"
PASSWORD = "123456"

@pytest.mark.order_flow
def test_place_order_login_before_checkout(page):
    logger = logging.getLogger(__name__)
    place_order = PlaceOrderPage(page)

    # Open homepage and login
    place_order.open_homepage()
    place_order.login(EMAIL, PASSWORD)
    assert place_order.verify_logged_in()
    logger.info("✅ Logged in successfully")

    # Add product and go to checkout
    place_order.add_product_to_cart()
    place_order.proceed_to_checkout()

    # Fill comment and place order
    place_order.fill_order_message_and_place_order()

    # Fill payment and submit
    place_order.fill_payment_details_and_submit()

    # Verify order success
    success_text = place_order.verify_order_success()
    assert "Your order has been placed" in success_text or "Congratulations" in success_text
    logger.info(f"✅ Order placed successfully: {success_text}")

    # Delete account

    # delete_msg = place_order.delete_account()
    # assert "Account Deleted" in delete_msg
    # logger.info("✅ Account deleted")






    # import logging
    # import pytest
    # import allure
    # from playwright.sync_api import expect
    #
    # EMAIL = "qa_testuser_01@example.com"
    # PASSWORD = "123456"
    #
    # @allure.suite("UI Tests")
    # @allure.title("Place Order: Login before Checkout")
    # @pytest.mark.order_flow
    # def test_place_order_login_before_checkout(page):
    #     logging.basicConfig(level=logging.INFO)
    #     logger = logging.getLogger(__name__)
    #
    #     page.goto("http://automationexercise.com")
    #     expect(page.locator("html")).to_be_visible()
    #
    #     page.locator("a[href='/login']").click()
    #     page.fill("input[data-qa='login-email']", EMAIL)
    #     page.fill("input[data-qa='login-password']", PASSWORD)
    #     page.locator("button[data-qa='login-button']").click()
    #     expect(page.locator("a:has-text('Logged in as')")).to_be_visible()
    #
    #     page.goto("https://automationexercise.com/products")
    #     page.hover("div.single-products")
    #     page.locator("a[data-product-id='1']").first.click()
    #     page.wait_for_selector("#cartModal")
    #     page.locator("button[data-dismiss='modal']").click()
    #
    #     page.locator("a[href='/view_cart']").first.click()
    #     page.get_by_text("Proceed To Checkout").click()
    #
    #     expect(page.locator("h2:has-text('Address Details')")).to_be_visible()
    #     expect(page.locator("h2:has-text('Review Your Order')")).to_be_visible()
    #
    #     page.locator("textarea[name='message']").fill("Please deliver ASAP")
    #
    #     page.locator("a[href='/payment']").click()
    #
    #     page.fill("input[name='name_on_card']", "QA Test User")
    #     page.fill("input[name='card_number']", "4111111111111111")
    #     page.fill("input[name='cvc']", "123")
    #     page.fill("input[name='expiry_month']", "12")
    #     page.fill("input[name='expiry_year']", "2026")
    #     page.locator("button#submit").click()
    #
    #     page.wait_for_timeout(3000)  # Wait for navigation / page render
    #     success_message = page.get_by_text("Congratulations! Your order has been confirmed!")
    #     expect(success_message).to_be_visible(timeout=10000)
    #     logger.info("Order confirmed message displayed.")

    # Delete account
    #
    # page.locator("a[href='/delete_account']").click()
    # expect(page.locator("h2")).to_have_text("Account Deleted!")
    # page.locator("a[data-qa='continue-button']").click()
