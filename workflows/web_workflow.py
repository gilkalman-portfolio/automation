from playwright.sync_api import Page
from utilities.manage_pages import Pages


class WebFlows:
    def __init__(self, page: Page):
        self.page = page
        self.pages = Pages(page)

    # --- Login ---

    def login(self, username: str, password: str):
        lp = self.pages.login_page
        lp.username_field.fill(username)
        lp.password_field.fill(password)
        lp.login_button.click()

    def login_valid(self):
        self.login("standard_user", "secret_sauce")

    def login_invalid_user(self):
        self.login("test", "test")

    # --- Products / Inventory ---

    def add_item_to_cart(self, slug: str):
        self.pages.inventory_page.add_to_cart(slug)

    def remove_item_from_inventory(self, slug: str):
        self.pages.inventory_page.remove_from_cart(slug)

    def sort_products(self, option_text: str):
        self.pages.inventory_page.sort_by(option_text)

    def go_to_cart(self):
        self.pages.inventory_page.cart_link.click()

    def logout(self):
        self.pages.inventory_page.logout()

    # --- Cart ---

    def remove_item_from_cart(self, slug: str):
        self.pages.cart_page.remove_item(slug)

    def proceed_to_checkout(self):
        self.pages.cart_page.proceed_to_checkout()

    # --- Checkout ---

    def fill_checkout_info(self, first_name: str, last_name: str, postal_code: str):
        self.pages.checkout_page.fill_info(first_name, last_name, postal_code)

    def finish_order(self):
        self.pages.checkout_page.finish_btn.click()

    # --- Full E2E flow ---

    def complete_purchase(self, slug: str, first_name="Test", last_name="User", postal_code="12345"):
        self.login_valid()
        self.add_item_to_cart(slug)
        self.go_to_cart()
        self.proceed_to_checkout()
        self.fill_checkout_info(first_name, last_name, postal_code)
        self.finish_order()



