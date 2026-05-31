import requests
from requests import Response


class UsersAPI:

    USERS = "/users"
    USER_BY_ID = "/users/{user_id}"

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def _url(self, path: str, **kwargs) -> str:
        return self.base_url + path.format(**kwargs)

    def get_all(self, params: dict | None = None) -> Response:
        return self.session.get(self._url(self.USERS), params=params)

    def get_by_id(self, user_id: int) -> Response:
        return self.session.get(self._url(self.USER_BY_ID, user_id=user_id))

    def create(self, name: str, email: str, gender: str, status: str) -> Response:
        payload = {"name": name, "email": email, "gender": gender, "status": status}
        return self.session.post(self._url(self.USERS), json=payload)

    def update(self, user_id: int, **fields) -> Response:
        return self.session.put(self._url(self.USER_BY_ID, user_id=user_id), json=fields)

    def delete(self, user_id: int) -> Response:
        return self.session.delete(self._url(self.USER_BY_ID, user_id=user_id))
