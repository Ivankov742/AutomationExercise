class PlaceOrderPage:
    def __init__(self, page):
        self.page = page

    def open_homepage(self):
        self.page.goto("http://automationexercise.com")

    def login(self, email, password):
        self.page.locator("a[href='/login']").click()
        self.page.fill("input[data-qa='login-email']", email)
        self.page.fill("input[data-qa='login-password']", password)
        self.page.locator("button[data-qa='login-button']").click()

    def verify_logged_in(self):
        return self.page.locator("a:has-text('Logged in as')").is_visible()

    def add_product_to_cart(self):
        self.page.goto("https://automationexercise.com/products")
        self.page.hover("div.single-products")
        self.page.locator("a[data-product-id='1']").first.click()
        self.page.wait_for_selector("#cartModal")
        self.page.locator("button[data-dismiss='modal']").click()

    def proceed_to_checkout(self):
        self.page.locator("a[href='/view_cart']").first.click()
        self.page.get_by_text("Proceed To Checkout").click()

    def fill_order_message_and_place_order(self):
        self.page.locator("textarea[name='message']").fill("Please deliver ASAP")
        self.page.locator("a[href='/payment']").click()

    def fill_payment_details_and_submit(self):
        self.page.fill("input[name='name_on_card']", "QA Test User")
        self.page.fill("input[name='card_number']", "4111111111111111")
        self.page.fill("input[name='cvc']", "123")
        self.page.fill("input[name='expiry_month']", "12")
        self.page.fill("input[name='expiry_year']", "2026")
        self.page.locator("button#submit").click()

    def verify_order_success(self):
        print("🔗 Current URL after payment:", self.page.url)
        self.page.screenshot(path="payment_debug.png")

        # Look for the success message by its text
        success_message = self.page.get_by_text("Congratulations! Your order has been confirmed!")

        success_message.wait_for(state="visible", timeout=10000)
        text = success_message.text_content()
        print(f"✅ Success message found: {text}")
        return text

    # def delete_account(self):
    #     self.page.locator("a[href='/delete_account']").click()
    #     return self.page.locator("h2").text_content()