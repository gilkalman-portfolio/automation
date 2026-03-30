import pytest
import allure
from playwright.sync_api import expect


BACKPACK = "sauce-labs-backpack"
BIKE_LIGHT = "sauce-labs-bike-light"
BOLT_TSHIRT = "sauce-labs-bolt-t-shirt"


@allure.suite("Saucedemo – Login")
class TestLogin:

    @allure.title("Valid login navigates to products page")
    @pytest.mark.smoke
    def test_valid_login(self, web_workflow):
        web_workflow.login_valid()
        expect(web_workflow.page).to_have_url("https://www.saucedemo.com/inventory.html")

    @allure.title("Locked out user sees error message")
    @pytest.mark.regression
    def test_locked_out_user(self, web_workflow):
        web_workflow.login("locked_out_user", "secret_sauce")
        expect(web_workflow.pages.login_page.error_message).to_be_visible()

    @allure.title("Invalid credentials shows error message")
    @pytest.mark.regression
    def test_invalid_credentials(self, web_workflow):
        web_workflow.login("wrong_user", "wrong_pass")
        expect(web_workflow.pages.login_page.error_message).to_be_visible()

    @allure.title("Empty username shows error message")
    @pytest.mark.regression
    def test_empty_username(self, web_workflow):
        web_workflow.login("", "secret_sauce")
        expect(web_workflow.pages.login_page.error_message).to_be_visible()

    @allure.title("Empty password shows error message")
    @pytest.mark.regression
    def test_empty_password(self, web_workflow):
        web_workflow.login("standard_user", "")
        expect(web_workflow.pages.login_page.error_message).to_be_visible()


@allure.suite("Saucedemo – Products")
class TestProducts:

    @pytest.fixture(autouse=True)
    def login(self, web_workflow):
        web_workflow.login_valid()

    @allure.title("Products page displays 6 items")
    @pytest.mark.smoke
    def test_product_count(self, web_workflow):
        expect(web_workflow.pages.inventory_page.inventory_items).to_have_count(6)

    @allure.title("Products page title is 'Products'")
    @pytest.mark.smoke
    def test_products_title(self, web_workflow):
        expect(web_workflow.pages.inventory_page.title).to_have_text("Products")

    @allure.title("Sort by Name Z to A")
    @pytest.mark.regression
    def test_sort_name_z_to_a(self, web_workflow):
        inv = web_workflow.pages.inventory_page
        inv.sort_by("Name (Z to A)")
        first_name = inv.item_names.first.inner_text()
        assert first_name == "Test.allTheThings() T-Shirt (Red)"

    @allure.title("Sort by Price low to high")
    @pytest.mark.regression
    def test_sort_price_low_to_high(self, web_workflow):
        inv = web_workflow.pages.inventory_page
        inv.sort_by("Price (low to high)")
        first_price = inv.item_prices.first.inner_text()
        assert first_price == "$7.99"

    @allure.title("Sort by Price high to low")
    @pytest.mark.regression
    def test_sort_price_high_to_low(self, web_workflow):
        inv = web_workflow.pages.inventory_page
        inv.sort_by("Price (high to low)")
        first_price = inv.item_prices.first.inner_text()
        assert first_price == "$49.99"


@allure.suite("Saucedemo – Cart")
class TestCart:

    @pytest.fixture(autouse=True)
    def login(self, web_workflow):
        web_workflow.login_valid()

    @allure.title("Cart badge shows 1 after adding one item")
    @pytest.mark.smoke
    def test_cart_badge_after_add(self, web_workflow):
        web_workflow.add_item_to_cart(BACKPACK)
        expect(web_workflow.pages.inventory_page.cart_badge).to_have_text("1")

    @allure.title("Cart badge shows 2 after adding two items")
    @pytest.mark.regression
    def test_cart_badge_two_items(self, web_workflow):
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.add_item_to_cart(BIKE_LIGHT)
        expect(web_workflow.pages.inventory_page.cart_badge).to_have_text("2")

    @allure.title("Cart contains added item")
    @pytest.mark.smoke
    def test_cart_contains_item(self, web_workflow):
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.go_to_cart()
        expect(web_workflow.pages.cart_page.cart_items).to_have_count(1)
        expect(web_workflow.pages.cart_page.item_names.first).to_have_text("Sauce Labs Backpack")

    @allure.title("Remove item from cart")
    @pytest.mark.regression
    def test_remove_item_from_cart(self, web_workflow):
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.go_to_cart()
        web_workflow.remove_item_from_cart(BACKPACK)
        expect(web_workflow.pages.cart_page.cart_items).to_have_count(0)

    @allure.title("Cart badge disappears after removing only item")
    @pytest.mark.regression
    def test_cart_badge_disappears_after_remove(self, web_workflow):
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.remove_item_from_inventory(BACKPACK)
        expect(web_workflow.pages.inventory_page.cart_badge).not_to_be_visible()


@allure.suite("Saucedemo – Checkout")
class TestCheckout:

    @pytest.fixture(autouse=True)
    def login_and_add(self, web_workflow):
        web_workflow.login_valid()
        web_workflow.add_item_to_cart(BACKPACK)
        web_workflow.go_to_cart()
        web_workflow.proceed_to_checkout()

    @allure.title("Checkout step one – missing first name shows error")
    @pytest.mark.regression
    def test_checkout_missing_first_name(self, web_workflow):
        web_workflow.pages.checkout_page.last_name_field.fill("User")
        web_workflow.pages.checkout_page.postal_code_field.fill("12345")
        web_workflow.pages.checkout_page.continue_btn.click()
        expect(web_workflow.pages.checkout_page.error_message).to_be_visible()

    @allure.title("Checkout step one – missing postal code shows error")
    @pytest.mark.regression
    def test_checkout_missing_postal_code(self, web_workflow):
        web_workflow.pages.checkout_page.first_name_field.fill("Test")
        web_workflow.pages.checkout_page.last_name_field.fill("User")
        web_workflow.pages.checkout_page.continue_btn.click()
        expect(web_workflow.pages.checkout_page.error_message).to_be_visible()

    @allure.title("Checkout step two – overview shows correct item total")
    @pytest.mark.smoke
    def test_checkout_overview_total(self, web_workflow):
        web_workflow.fill_checkout_info("Test", "User", "12345")
        expect(web_workflow.pages.checkout_page.subtotal_label).to_contain_text("29.99")

    @allure.title("E2E – complete purchase shows confirmation")
    @pytest.mark.smoke
    def test_complete_purchase(self, web_workflow):
        web_workflow.fill_checkout_info("Test", "User", "12345")
        web_workflow.finish_order()
        expect(web_workflow.pages.checkout_page.complete_header).to_have_text("Thank you for your order!")
        expect(web_workflow.page).to_have_url("https://www.saucedemo.com/checkout-complete.html")


@allure.suite("Saucedemo – Navigation")
class TestNavigation:

    @pytest.fixture(autouse=True)
    def login(self, web_workflow):
        web_workflow.login_valid()

    @allure.title("Logout redirects to login page")
    @pytest.mark.smoke
    def test_logout(self, web_workflow):
        web_workflow.logout()
        expect(web_workflow.page).to_have_url("https://www.saucedemo.com/")
        expect(web_workflow.pages.login_page.login_button).to_be_visible()
