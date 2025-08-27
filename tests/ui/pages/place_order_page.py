from playwright.sync_api import Page, expect

class PlaceOrderLocators:
    LOGIN_LINK = "a[href='/login']"
    LOGIN_EMAIL = "input[data-qa='login-email']"
    LOGIN_PASS = "input[data-qa='login-password']"
    LOGIN_BTN  = "button[data-qa='login-button']"
    LOGGED_IN_AS = "a:has-text('Logged in as')"

    PRODUCTS_LINK = "a[href='/products']"
    PRODUCT_CARD = "div.single-products"
    ADD_TO_CART = "a[data-product-id='1']"
    CART_MODAL  = "#cartModal"
    MODAL_CLOSE = "button[data-dismiss='modal']"

    VIEW_CART = "a[href='/view_cart']"
    PROCEED_CHECKOUT_BTN = "text=Proceed To Checkout"

    MESSAGE_TEXTAREA = "textarea[name='message']"
    PAYMENT_LINK = "a[href='/payment']"

    NAME_ON_CARD = "input[name='name_on_card']"
    CARD_NUMBER  = "input[name='card_number']"
    CVC          = "input[name='cvc']"
    EXP_MONTH    = "input[name='expiry_month']"
    EXP_YEAR     = "input[name='expiry_year']"
    PAY_BTN      = "button#submit"

    SUCCESS_TEXT = "text=Congratulations! Your order has been confirmed!"
    DELETE_ACC   = "a[href='/delete_account']"
    H2           = "h2"


class PlaceOrderPage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    # ---- Actions ----
    def open_homepage(self):
        candidates = [self.base_url]
        if self.base_url.startswith("https://"):
            candidates.append(self.base_url.replace("https://", "http://", 1))
        last_err = None
        for url in candidates:
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                self.page.wait_for_selector(PlaceOrderLocators.LOGIN_LINK, timeout=30000)
                return
            except Exception as e:
                last_err = e
        raise AssertionError(f"Failed to open homepage via https/http: {last_err}")

    def login(self, email: str, password: str):
        self.page.locator(PlaceOrderLocators.LOGIN_LINK).click()
        self.page.fill(PlaceOrderLocators.LOGIN_EMAIL, email)
        self.page.fill(PlaceOrderLocators.LOGIN_PASS, password)
        self.page.locator(PlaceOrderLocators.LOGIN_BTN).click()

    def add_product_to_cart(self):
        self.page.locator(PlaceOrderLocators.PRODUCTS_LINK).click()
        self.page.wait_for_url("**/products", timeout=30000)
        self.page.wait_for_selector(PlaceOrderLocators.PRODUCT_CARD, state="visible", timeout=30000)
        self.page.locator(PlaceOrderLocators.PRODUCT_CARD).first.scroll_into_view_if_needed()
        self.page.hover(PlaceOrderLocators.PRODUCT_CARD)
        self.page.locator(PlaceOrderLocators.ADD_TO_CART).first.click()
        self.page.wait_for_selector(PlaceOrderLocators.CART_MODAL, state="visible", timeout=30000)
        self.page.locator(PlaceOrderLocators.MODAL_CLOSE).click()

    def proceed_to_checkout(self):
        self.page.locator(PlaceOrderLocators.VIEW_CART).first.click()
        self.page.wait_for_url("**/view_cart", timeout=30000)
        self.page.locator(PlaceOrderLocators.PROCEED_CHECKOUT_BTN).click()

    def fill_order_message_and_go_to_payment(self, message: str = "Please deliver ASAP"):
        self.page.locator(PlaceOrderLocators.MESSAGE_TEXTAREA).fill(message)
        self.page.locator(PlaceOrderLocators.PAYMENT_LINK).click()

    def fill_payment_details_and_submit(self, payment: dict):
        self.page.fill(PlaceOrderLocators.NAME_ON_CARD, payment["name_on_card"])
        self.page.fill(PlaceOrderLocators.CARD_NUMBER,  payment["card_number"])
        self.page.fill(PlaceOrderLocators.CVC,          payment["cvc"])
        self.page.fill(PlaceOrderLocators.EXP_MONTH,    payment["expiry_month"])
        self.page.fill(PlaceOrderLocators.EXP_YEAR,     payment["expiry_year"])
        self.page.locator(PlaceOrderLocators.PAY_BTN).click()

    # ---- Checks ----
    def should_be_logged_in(self):
        expect(self.page.locator(PlaceOrderLocators.LOGGED_IN_AS)).to_be_visible()

    def should_be_on_checkout(self, base_url: str):
        expect(self.page).to_have_url(f"{base_url.rstrip('/')}/checkout")

    def should_see_success_message(self):
        expect(self.page.locator(PlaceOrderLocators.SUCCESS_TEXT)).to_be_visible(timeout=10000)

    def delete_account(self):
        self.page.locator(PlaceOrderLocators.DELETE_ACC).click()
        return self.page.locator(PlaceOrderLocators.H2).text_content()
