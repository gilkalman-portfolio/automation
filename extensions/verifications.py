import allure
from playwright.sync_api import Locator


class Verifications:

    @staticmethod
    @allure.step("Verify text equals")
    def verify_equals(actual, expected):
        assert actual == expected, f"Expected '{expected}', got '{actual}'"

    @staticmethod
    @allure.step("Verify element is visible")
    def is_visible(elem: Locator):
        assert elem.is_visible(), "Element is not visible"

    @staticmethod
    @allure.step("Soft verify multiple elements are visible")
    def soft_visible(elems: Locator):
        failed = []
        count = elems.count()
        for i in range(count):
            if not elems.nth(i).is_visible():
                failed.append(i)
        if failed:
            raise AssertionError(f"Elements not visible at indexes: {failed}")

    @staticmethod
    @allure.step("Verify number of elements")
    def verify_count(elems: Locator, expected: int):
        assert elems.count() == expected, f"Expected {expected} items, got {elems.count()}"

    @staticmethod
    @allure.step("Verify at least N elements exist")
    def verify_at_least(elems: Locator, n: int = 1):
        assert elems.count() >= n, f"Expected at least {n} items, got {elems.count()}"
