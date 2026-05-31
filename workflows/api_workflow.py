from api_objects.users_api import UsersAPI


class APIFlows:

    def __init__(self, base_url: str, token: str):
        self.users = UsersAPI(base_url, token)

    def create_user(self, name: str, email: str, gender: str = "male", status: str = "active") -> dict:
        resp = self.users.create(name, email, gender, status)
        assert resp.status_code == 201, f"Expected 201, got {resp.status_code}: {resp.text}"
        return resp.json()

    def get_user(self, user_id: int) -> dict:
        resp = self.users.get_by_id(user_id)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        return resp.json()

    def update_user(self, user_id: int, **fields) -> dict:
        resp = self.users.update(user_id, **fields)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}: {resp.text}"
        return resp.json()

    def delete_user(self, user_id: int) -> None:
        resp = self.users.delete(user_id)
        assert resp.status_code == 204, f"Expected 204, got {resp.status_code}"

    def create_and_verify(self, name: str, email: str, gender: str = "male", status: str = "active") -> dict:
        created = self.create_user(name, email, gender, status)
        fetched = self.get_user(created["id"])
        assert fetched["name"] == name
        assert fetched["email"] == email
        return created

    def full_crud_cycle(self, name: str, email: str) -> None:
        user = self.create_user(name, email)
        user_id = user["id"]

        self.get_user(user_id)
        self.update_user(user_id, name="Updated Name")

        updated = self.get_user(user_id)
        assert updated["name"] == "Updated Name"

        self.delete_user(user_id)

        resp = self.users.get_by_id(user_id)
        assert resp.status_code == 404
