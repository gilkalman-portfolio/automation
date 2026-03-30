from playwright.sync_api import Page, Locator


class CheckoutPage:
    """Page Object for Saucedemo Checkout Pages (step-one, step-two, complete)"""

    # Step One
    TITLE = '[data-test="title"]'
    FIRST_NAME = '[data-test="firstName"]'
    LAST_NAME = '[data-test="lastName"]'
    POSTAL_CODE = '[data-test="postalCode"]'
    CONTINUE_BTN = '[data-test="continue"]'
    CANCEL_BTN = '[data-test="cancel"]'
    ERROR_MESSAGE = '[data-test="error"]'

    # Step Two (Overview)
    SUBTOTAL_LABEL = '[data-test="subtotal-label"]'
    TAX_LABEL = '[data-test="tax-label"]'
    TOTAL_LABEL = '[data-test="total-label"]'
    FINISH_BTN = '[data-test="finish"]'

    # Complete
    COMPLETE_HEADER = '[data-test="complete-header"]'
    COMPLETE_TEXT = '[data-test="complete-text"]'
    BACK_HOME_BTN = '[data-test="back-to-products"]'

    def __init__(self, page: Page):
        self.page = page

    # Step One properties
    @property
    def title(self) -> Locator:
        return self.page.locator(self.TITLE)

    @property
    def first_name_field(self) -> Locator:
        return self.page.locator(self.FIRST_NAME)

    @property
    def last_name_field(self) -> Locator:
        return self.page.locator(self.LAST_NAME)

    @property
    def postal_code_field(self) -> Locator:
        return self.page.locator(self.POSTAL_CODE)

    @property
    def continue_btn(self) -> Locator:
        return self.page.locator(self.CONTINUE_BTN)

    @property
    def cancel_btn(self) -> Locator:
        return self.page.locator(self.CANCEL_BTN)

    @property
    def error_message(self) -> Locator:
        return self.page.locator(self.ERROR_MESSAGE)

    # Step Two properties
    @property
    def subtotal_label(self) -> Locator:
        return self.page.locator(self.SUBTOTAL_LABEL)

    @property
    def tax_label(self) -> Locator:
        return self.page.locator(self.TAX_LABEL)

    @property
    def total_label(self) -> Locator:
        return self.page.locator(self.TOTAL_LABEL)

    @property
    def finish_btn(self) -> Locator:
        return self.page.locator(self.FINISH_BTN)

    # Complete properties
    @property
    def complete_header(self) -> Locator:
        return self.page.locator(self.COMPLETE_HEADER)

    @property
    def back_home_btn(self) -> Locator:
        return self.page.locator(self.BACK_HOME_BTN)

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_field.fill(first_name)
        self.last_name_field.fill(last_name)
        self.postal_code_field.fill(postal_code)
        self.continue_btn.click()
