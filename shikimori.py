from typing import Callable, Mapping, Sequence, Optional, Any
import functools
import re

from requests_oauthlib import OAuth2Session


class Shikimori:
    SHIKIMORI_URL: str = 'https://shikimori.one'
    _TOKEN_URL = SHIKIMORI_URL + '/oauth/token'

    def __init__(self,
                 app_name:      Optional[str] = None,
                 *,
                 client_id:     Optional[str] = None,
                 client_secret: Optional[str] = None,
                 token:         Optional[Mapping] = None,
                 redirect_uri:  str = 'urn:ietf:wg:oauth:2.0:oob',
                 token_saver:   Optional[Callable[[dict], Any]] = None,
                 scope:         Optional[Sequence[str]] = None
                 ) -> None:

        self._client_id = client_id
        self._client_secret = client_secret
        self._token_saver = token_saver or (lambda d: None)
        self._headers = {
            'User-Agent': app_name,
        }
        self._extra = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
        }
        self._client = OAuth2Session(self._client_id, auto_refresh_url=self._TOKEN_URL, auto_refresh_kwargs=self._extra,
                               scope=scope, redirect_uri=redirect_uri, token=token, token_updater=self._token_saver)
        self._client.headers.update(self._headers)
        self.authorize()
        self.user_id = self._client.get("https://shikimori.one/api/users/whoami").json()["id"]

    def authorize(self):
        auth_url = self.SHIKIMORI_URL + '/oauth/authorize'
        print(self._client.authorization_url(auth_url)[0])
        code = input()
        self.fetch_token(code)

    def fetch_token(self, code: str) -> dict:
        self._client.fetch_token(self._TOKEN_URL, code, client_secret=self._client_secret)
        self._token_saver(self.token)
        return self.token

    @property
    def token(self) -> dict:
        return self._client.token

    def get_data(self, path):
        return self._client.get(path).json()

    def get_user_data(self) -> list:
        return self._client.get(f"{self.SHIKIMORI_URL}/api/v2/user_rates?limit=10").json()

    def get_user_anime(self) -> list:
        return self._client.get(f"{self.SHIKIMORI_URL}/api/users/{self.user_id}/anime_rates?limit=5000").json()

    def get_user_manga(self) -> list:
        return self._client.get(f"{self.SHIKIMORI_URL}/api/users//{self.user_id}/manga_rates?limit=5000").json()

