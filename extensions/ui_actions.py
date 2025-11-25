import allure
from playwright.sync_api import Page, Locator


class UiActions:

    @staticmethod
    @allure.step("Click element")
    def click(elem: Locator):
        elem.click()

    @staticmethod
    @allure.step("Type text")
    def type_text(elem: Locator, value: str, delay: float = 0):
        elem.fill("")
        if delay:
            for c in value:
                elem.type(c, delay=delay)
        else:
            elem.fill(value)

    @staticmethod
    @allure.step("Hover over element")
    def hover(elem: Locator):
        elem.hover()

    @staticmethod
    @allure.step("Right click element")
    def right_click(elem: Locator):
        elem.click(button="right")

    @staticmethod
    @allure.step("Drag and drop")
    def drag_and_drop(source: Locator, target: Locator):
        source.drag_to(target)

    @staticmethod
    @allure.step("Scroll to bottom")
    def scroll_to_bottom(page: Page):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    @staticmethod
    @allure.step("Navigate back")
    def back(page: Page):
        page.go_back()

    @staticmethod
    @allure.step("Press TAB")
    def press_tab(page: Page):
        page.keyboard.press("Tab")
