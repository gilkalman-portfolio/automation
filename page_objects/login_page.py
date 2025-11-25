from playwright.sync_api import Page, Locator


class LoginPage:
    """Page Object for Saucedemo Login Page (https://www.saucedemo.com/)"""

    # Locators using data-test attributes
    USERNAME_INPUT = '[data-test="username"]'
    PASSWORD_INPUT = '[data-test="password"]'
    LOGIN_BUTTON = '[data-test="login-button"]'
    ERROR_MESSAGE = '[data-test="error"]'


    def __init__(self, page: Page):
        self.page = page

    # Element getters
    @property
    def username_field(self) -> Locator:
        """Get username input field"""
        return self.page.locator(self.USERNAME_INPUT)

    @property
    def password_field(self) -> Locator:
        """Get password input field"""
        return self.page.locator(self.PASSWORD_INPUT)

    @property
    def login_button(self) -> Locator:
        """Get login button"""
        return self.page.locator(self.LOGIN_BUTTON)

    @property
    def error_message(self) -> Locator:
        """Get error message element"""
        return self.page.locator(self.ERROR_MESSAGE)


