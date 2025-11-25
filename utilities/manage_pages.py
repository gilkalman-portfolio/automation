from playwright.sync_api import Page
from page_objects.login_page import LoginPage


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

