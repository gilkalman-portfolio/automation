from playwright.sync_api import Page
from utilities.manage_pages import Pages


class WebFlows:
    def __init__(self, page:Page):
        self.page = page
        self.pages = Pages(page)

    def login(self, username: str, password: str):
        lp = self.pages.login_page
        lp.username_field.fill(username)
        lp.password_field.fill(password)
        lp.login_button.click()

    def login_valid(self):
        self.login("standard_user", "secret_sauce")

    def login_invalid_user(self):
        self.login("test", "test")



