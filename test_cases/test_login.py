import pytest
import allure
from playwright.sync_api import Page, expect
from page_objects.login_page import LoginPage
from workflows import web_workflow
from workflows.web_workflow import WebFlows


@allure.suite("Login")
@pytest.mark.smoke
class TestLogin:

    @allure.title("Login – valid user")
    @allure.description("Login with a valid user should navigate to the products page")
    @pytest.mark.smoke
    def test_verified_login(self, web_workflow):
        web_workflow.login_valid()

    def test_non_verified_login(self, web_workflow):
       web_workflow.login_invalid_user()