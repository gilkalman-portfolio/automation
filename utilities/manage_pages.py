from playwright.sync_api import Page

#from api_objects.users_api import UsersApi
from page_objects.login_page import LoginPage
from page_objects.inventory_page import InventoryPage
from page_objects.cart_page import CartPage
from page_objects.checkout_page import CheckoutPage


class Pages:
    """
    Central manager for all Page Objects.

    Usage in flows/tests:
        pages = Pages(page)
        pages.login_page.username_field.fill("standard_user")
    """

    def __init__(self, page: Page):
        self.page = page

        # Page Objects
        self.login_page = LoginPage(page)
        self.inventory_page = InventoryPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)



