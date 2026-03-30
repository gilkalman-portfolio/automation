from playwright.sync_api import Page, Locator


class InventoryPage:
    """Page Object for Saucedemo Inventory/Products Page (https://www.saucedemo.com/inventory.html)"""

    TITLE = '[data-test="title"]'
    SORT_DROPDOWN = '[data-test="product-sort-container"]'
    INVENTORY_ITEM = '[data-test="inventory-item"]'
    ITEM_NAME = '[data-test="inventory-item-name"]'
    ITEM_PRICE = '[data-test="inventory-item-price"]'
    CART_BADGE = '[data-test="shopping-cart-badge"]'
    CART_LINK = '[data-test="shopping-cart-link"]'
    BURGER_MENU = '#react-burger-menu-btn'
    LOGOUT_LINK = '[data-test="logout-sidebar-link"]'
    ALL_ITEMS_LINK = '[data-test="inventory-sidebar-link"]'
    RESET_LINK = '[data-test="reset-sidebar-link"]'
    ADD_TO_CART_BTN = '[data-test="add-to-cart-{slug}"]'
    REMOVE_BTN = '[data-test="remove-{slug}"]'

    def __init__(self, page: Page):
        self.page = page

    @property
    def title(self) -> Locator:
        return self.page.locator(self.TITLE)

    @property
    def sort_dropdown(self) -> Locator:
        return self.page.locator(self.SORT_DROPDOWN)

    @property
    def inventory_items(self) -> Locator:
        return self.page.locator(self.INVENTORY_ITEM)

    @property
    def item_names(self) -> Locator:
        return self.page.locator(self.ITEM_NAME)

    @property
    def item_prices(self) -> Locator:
        return self.page.locator(self.ITEM_PRICE)

    @property
    def cart_badge(self) -> Locator:
        return self.page.locator(self.CART_BADGE)

    @property
    def cart_link(self) -> Locator:
        return self.page.locator(self.CART_LINK)

    @property
    def burger_menu(self) -> Locator:
        return self.page.locator(self.BURGER_MENU)

    @property
    def logout_link(self) -> Locator:
        return self.page.locator(self.LOGOUT_LINK)

    def add_to_cart(self, slug: str) -> None:
        self.page.locator(self.ADD_TO_CART_BTN.format(slug=slug)).click()

    def remove_from_cart(self, slug: str) -> None:
        self.page.locator(self.REMOVE_BTN.format(slug=slug)).click()

    def sort_by(self, option_text: str) -> None:
        self.sort_dropdown.select_option(label=option_text)

    def open_menu(self) -> None:
        self.burger_menu.click()

    def logout(self) -> None:
        self.open_menu()
        self.logout_link.click()
