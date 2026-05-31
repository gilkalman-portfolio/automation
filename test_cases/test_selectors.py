import pytest
import allure
from playwright.sync_api import expect


BACKPACK = "sauce-labs-backpack"


@allure.suite("Page Object Selectors – Login Page")
class TestLoginSelectors:

    @allure.title("Login page has username field")
    @pytest.mark.sanity
    def test_username_field(self, web_workflow):
        expect(web_workflow.pages.login_page.username_field).to_be_visible()

    @allure.title("Login page has password field")
    @pytest.mark.sanity
    def test_password_field(self, web_workflow):
        expect(web_workflow.pages.login_page.password_field).to_be_visible()

    @allure.title("Login page has login button")
    @pytest.mark.sanity
    def test_login_button(self, web_workflow):
        expect(web_workflow.pages.login_page.login_button).to_be_visible()

    @allure.title("Login page shows error on bad credentials")
    @pytest.mark.sanity
    def test_error_message(self, web_workflow):
        web_workflow.login("bad", "bad")
        expect(web_workflow.pages.login_page.error_message).to_be_visible()


@allure.suite("Page Object Selectors – Inventory Page")
class TestInventorySelectors:

    @pytest.fixture(autouse=True)
    def login(self, web_workflow):
        web_workflow.login_valid()

    @allure.title("Inventory page has title")
    @pytest.mark.sanity
    def test_title(self, web_workflow):
        expect(web_workflow.pages.inventory_page.title).to_be_visible()

    @allure.title("Inventory page has sort dropdown")
    @pytest.mark.sanity
    def test_sort_dropdown(self, web_workflow):
        expect(web_workflow.pages.inventory_page.sort_dropdown).to_be_visible()

    @allure.title("Inventory page has product items")
    @pytest.mark.sanity
    def test_inventory_items(self, web_workflow):
        expect(web_workflow.pages.inventory_page.inventory_items.first).to_be_visible()

    @allure.title("Inventory page has item names")
    @pytest.mark.sanity
    def test_item_names(self, web_workflow):
        expect(web_workflow.pages.inventory_page.item_names.first).to_be_visible()

    @allure.title("Inventory page has item prices")
    @pytest.mark.sanity
    def test_item_prices(self, web_workflow):
        expect(web_workflow.pages.inventory_page.item_prices.first).to_be_visible()

    @allure.title("Inventory page has cart link")
    @pytest.mark.sanity
    def test_cart_link(self, web_workflow):
        expect(web_workflow.pages.inventory_page.cart_link).to_be_visible()

    @allure.title("Inventory page has burger menu")
    @pytest.mark.sanity
    def test_burger_menu(self, web_workflow):
        expect(web_workflow.pages.inventory_page.burger_menu).to_be_visible()

    @allure.title("Inventory page has add-to-cart button")
    @pytest.mark.sanity
    def test_add_to_cart_btn(self, web_workflow):
        selector = web_workflow.pages.inventory_page.ADD_TO_CART_BTN.format(slug=BACKPACK)
        expect(web_workflow.page.locator(selector)).to_be_visible()


@allure.suite("Page Object Selectors – Cart Page")
class TestCartSelectors:

    @pytest.fixture(autouse=True)
    def setup(self, web_workflow):
        web_workflow.login_valid()
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.go_to_cart()

    @allure.title("Cart page has title")
    @pytest.mark.sanity
    def test_title(self, web_workflow):
        expect(web_workflow.pages.cart_page.title).to_be_visible()

    @allure.title("Cart page has cart items")
    @pytest.mark.sanity
    def test_cart_items(self, web_workflow):
        expect(web_workflow.pages.cart_page.cart_items.first).to_be_visible()

    @allure.title("Cart page has item name")
    @pytest.mark.sanity
    def test_item_name(self, web_workflow):
        expect(web_workflow.pages.cart_page.item_names.first).to_be_visible()

    @allure.title("Cart page has item price")
    @pytest.mark.sanity
    def test_item_price(self, web_workflow):
        expect(web_workflow.pages.cart_page.item_prices.first).to_be_visible()

    @allure.title("Cart page has continue shopping button")
    @pytest.mark.sanity
    def test_continue_shopping_btn(self, web_workflow):
        expect(web_workflow.pages.cart_page.continue_shopping_btn).to_be_visible()

    @allure.title("Cart page has checkout button")
    @pytest.mark.sanity
    def test_checkout_btn(self, web_workflow):
        expect(web_workflow.pages.cart_page.checkout_btn).to_be_visible()


@allure.suite("Page Object Selectors – Checkout Page")
class TestCheckoutSelectors:

    @pytest.fixture(autouse=True)
    def setup(self, web_workflow):
        web_workflow.login_valid()
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.go_to_cart()
        web_workflow.proceed_to_checkout()

    @allure.title("Checkout page has title")
    @pytest.mark.sanity
    def test_title(self, web_workflow):
        expect(web_workflow.pages.checkout_page.title).to_be_visible()

    @allure.title("Checkout page has first name field")
    @pytest.mark.sanity
    def test_first_name_field(self, web_workflow):
        expect(web_workflow.pages.checkout_page.first_name_field).to_be_visible()

    @allure.title("Checkout page has last name field")
    @pytest.mark.sanity
    def test_last_name_field(self, web_workflow):
        expect(web_workflow.pages.checkout_page.last_name_field).to_be_visible()

    @allure.title("Checkout page has postal code field")
    @pytest.mark.sanity
    def test_postal_code_field(self, web_workflow):
        expect(web_workflow.pages.checkout_page.postal_code_field).to_be_visible()

    @allure.title("Checkout page has continue button")
    @pytest.mark.sanity
    def test_continue_btn(self, web_workflow):
        expect(web_workflow.pages.checkout_page.continue_btn).to_be_visible()

    @allure.title("Checkout page has cancel button")
    @pytest.mark.sanity
    def test_cancel_btn(self, web_workflow):
        expect(web_workflow.pages.checkout_page.cancel_btn).to_be_visible()
