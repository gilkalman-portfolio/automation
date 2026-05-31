import uuid

import pytest
import allure
import requests

from workflows.api_workflow import APIFlows

API_BASE = "https://gorest.co.in/public/v2"


def _api_reachable() -> bool:
    try:
        resp = requests.get(f"{API_BASE}/users", timeout=5)
        return resp.status_code != 403
    except requests.RequestException:
        return False


def _unique_email() -> str:
    return f"test_{uuid.uuid4().hex[:8]}@testing.com"


_skip_reason = "GoRest API not reachable (Cloudflare block)"


@allure.suite("GoRest API – Users")
@pytest.mark.skipif(not _api_reachable(), reason=_skip_reason)
class TestUsersAPI:

    @allure.title("GET /users returns a list of users")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_users(self, api_workflow: APIFlows):
        resp = api_workflow.users.get_all()
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @allure.title("GET /users supports pagination")
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_users_pagination(self, api_workflow: APIFlows):
        resp = api_workflow.users.get_all(params={"page": 1, "per_page": 5})
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) <= 5

    @allure.title("POST /users creates a new user")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_user(self, api_workflow: APIFlows):
        user = api_workflow.create_user(
            name="Test Automation",
            email=_unique_email(),
        )
        assert user["id"] is not None
        assert user["name"] == "Test Automation"
        assert user["status"] == "active"

        api_workflow.delete_user(user["id"])

    @allure.title("GET /users/{id} returns correct user")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_single_user(self, api_workflow: APIFlows):
        created = api_workflow.create_user("Fetch Me", _unique_email())
        fetched = api_workflow.get_user(created["id"])

        assert fetched["id"] == created["id"]
        assert fetched["name"] == "Fetch Me"

        api_workflow.delete_user(created["id"])

    @allure.title("PUT /users/{id} updates user fields")
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_user(self, api_workflow: APIFlows):
        user = api_workflow.create_user("Before Update", _unique_email())
        updated = api_workflow.update_user(user["id"], name="After Update")

        assert updated["name"] == "After Update"

        api_workflow.delete_user(user["id"])

    @allure.title("DELETE /users/{id} removes the user")
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_user(self, api_workflow: APIFlows):
        user = api_workflow.create_user("Delete Me", _unique_email())
        api_workflow.delete_user(user["id"])

        resp = api_workflow.users.get_by_id(user["id"])
        assert resp.status_code == 404

    @allure.title("GET /users/{id} returns 404 for non-existent user")
    @pytest.mark.regression
    @pytest.mark.api
    def test_get_nonexistent_user(self, api_workflow: APIFlows):
        resp = api_workflow.users.get_by_id(9999999)
        assert resp.status_code == 404

    @allure.title("POST /users with invalid email returns 422")
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_user_invalid_email(self, api_workflow: APIFlows):
        resp = api_workflow.users.create(
            name="Bad Email",
            email="not-an-email",
            gender="male",
            status="active",
        )
        assert resp.status_code == 422

    @allure.title("POST /users with missing fields returns 422")
    @pytest.mark.regression
    @pytest.mark.api
    def test_create_user_missing_fields(self, api_workflow: APIFlows):
        resp = api_workflow.users.create(name="", email="", gender="", status="")
        assert resp.status_code == 422

    @allure.title("E2E – full CRUD cycle on a single user")
    @pytest.mark.smoke
    @pytest.mark.api
    def test_full_crud_cycle(self, api_workflow: APIFlows):
        api_workflow.full_crud_cycle(
            name="CRUD Test",
            email=_unique_email(),
        )
