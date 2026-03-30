from playwright.sync_api import Page, Locator


class CartPage:
    """Page Object for Saucedemo Cart Page (https://www.saucedemo.com/cart.html)"""

    TITLE = '[data-test="title"]'
    CART_ITEM = '[data-test="inventory-item"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    ITEM_QUANTITY = '[data-test="item-quantity"]'
    CONTINUE_SHOPPING_BTN = '[data-test="continue-shopping"]'
    CHECKOUT_BTN = '[data-test="checkout"]'
    REMOVE_BTN = '[data-test="remove-{slug}"]'

    def __init__(self, page: Page):
        self.page = page

    @property
    def title(self) -> Locator:
        return self.page.locator(self.TITLE)

    @property
    def cart_items(self) -> Locator:
        return self.page.locator(self.CART_ITEM)

    @property
    def item_names(self) -> Locator:
        return self.page.locator(self.ITEM_NAME)

    @property
    def item_prices(self) -> Locator:
        return self.page.locator(self.ITEM_PRICE)

    @property
    def continue_shopping_btn(self) -> Locator:
        return self.page.locator(self.CONTINUE_SHOPPING_BTN)

    @property
    def checkout_btn(self) -> Locator:
        return self.page.locator(self.CHECKOUT_BTN)

    def remove_item(self, slug: str) -> None:
        self.page.locator(self.REMOVE_BTN.format(slug=slug)).click()

    def proceed_to_checkout(self) -> None:
        self.checkout_btn.click()
