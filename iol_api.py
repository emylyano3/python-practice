import requests as r
from token_manager import TokenManager


class IolApi:

    def __init__(self, config, token_manager: TokenManager):
        self._config = config
        self._token_manager = token_manager
        pass

    def get_portfolio(self, country):
        api_url = f'{self._config.get("base_url")}{self._config.get("api_path")}/portafolio/{country}'
        return r.get(api_url, headers={"Authorization": f'Bearer {self._token_manager.get_token()}'}).json()
