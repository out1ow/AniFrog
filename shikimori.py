import json
from tkinter.font import names
from typing import Mapping, Sequence, Optional

import requests
from requests_oauthlib import OAuth2Session


def token_saver(token: dict):
    with open("token.json", 'w') as f:
        f.write(json.dumps(token))


class Shikimori:
    SHIKIMORI_URL: str = 'https://shikimori.one'
    _TOKEN_URL = SHIKIMORI_URL + '/oauth/token'

    def __init__(self,
                 app_name:      Optional[str] = None,
                 *,
                 client_id:     Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token:         Optional[Mapping] = None,
                 redirect_uri:  str = 'urn:ietf:wg:oauth:2.0:oob'
                 ) -> None:

        self._client_id = client_id
        self._client_secret = client_secret
        self._headers = {
            'User-Agent': app_name,
        }
        self._extra = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        self._client = OAuth2Session(self._client_id, auto_refresh_url=self._TOKEN_URL, auto_refresh_kwargs=self._extra,
                                     scope=["user_rates"], redirect_uri=redirect_uri, token=token, token_updater=token_saver)
        self._client.headers.update(self._headers)
        if token == None: self.authorize()
        self._user_id = self._client.get("https://shikimori.one/api/users/whoami").json()["id"]

    def authorize(self):
        auth_url = self.SHIKIMORI_URL + '/oauth/authorize'
        print(self._client.authorization_url(auth_url)[0])
        code = input()
        self.fetch_token(code)

    def fetch_token(self, code: str) -> dict:
        self._client.fetch_token(self._TOKEN_URL, code, client_secret=self._client_secret)
        token_saver(self.token)
        return self.token

    @property
    def token(self) -> dict:
        return self._client.token

#========================================================================

    def get_data(self, path):
        return self._client.get(path).json()

    def get_user_data(self) -> list:
        return self._client.get(f"{self.SHIKIMORI_URL}/api/users/{self._user_id}").json()

    def get_user_anime(self, status: str='') -> list:
        params = {
            "limit": 500,
             "status": status
        }
        return self._client.get(f"{self.SHIKIMORI_URL}/api/users/{self._user_id}/anime_rates", params=params).json()

    def get_anime(self, name: str, limit: int=1) -> list:
        params = {
            "search": name,
            "limit": limit
        }
        return self._client.get(f"{self.SHIKIMORI_URL}/api/animes/", params=params).json()

    def get_anime_id(self, name: str) -> dict:
        params = {
            "search": name
        }
        i = self._client.get(f"{self.SHIKIMORI_URL}/api/animes/", params=params).json()[0]['id']
        return self._client.get(f"{self.SHIKIMORI_URL}/api/animes/{i}", params=params).json()

    # TODO: придумать что-то с превьюшками анимешек

    # def get_anime_preview(self, name: str) -> str:
    #     data = self.get_anime(name)
    #     url = "https://shikimori.one" + data[0]["image"]["preview"]
    #     img = requests.get(url).content
    #     f = open(f"src/previews/{data[0]['id']}.jpg", "wb")
    #     f.write(img)
    #     f.close()
    #     return f"/src/previews/{data[0]['id']}.jpg"

#========================================================================

    # TODO: реализовать методы POST для изменения пользовательского списка
    def post_user_anime(self, name: str):
        params = {
            "user_rate": {
                "score": "10",
                "target_id": 263,
                "text": "test",
                "user_id": self._user_id
            }
        }
        return self._client.post(f"{self.SHIKIMORI_URL}/api/v2/user_rates/{self._user_id}/increment")
