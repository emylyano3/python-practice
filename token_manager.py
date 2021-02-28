import time
import requests as r


class TokenManager:

    def __init__(self, config, credential_manager):
        print("Initializing token manager")
        self._cm = credential_manager
        if not self._cm.user or not self._cm.password:
            raise Exception("Credentials not entered")
        _data = {
            "username": self._cm.user,
            "password": self._cm.password,
            "grant_type": "password"
        }
        print("Getting token")
        self._config = config
        self.__ask_for_token(_data)

    def get_token(self):
        if self.__token_expired():
            print("Token expired. Refreshing it.")
            _data = {
                "refresh_token": self.token_data["refresh_token"],
                "grant_type": "refresh_token"
            }
            self.__ask_for_token(_data)
            return self.token_data["access_token"]
        else:
            return self.token_data["access_token"]

    def __token_expired(self):
        ttl = self.token_data["expires_in"]
        if time.time() - self.last < ttl:
            return False
        else:
            return True

    def __ask_for_token(self, _data):
        api_url = f'{self._config.get("base_url")}/token'
        response = r.post(api_url, data=_data)
        if response.status_code == 200:
            self.last = time.time()
            self.token_data = response.json()
        else:
            raise Exception("Error getting token " + str(response.status_code))
