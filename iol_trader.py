import requests as r
import time

api_base_url = "https://api.invertironline.com"


class CredentialManager:

    def __init__(self):
        self.user = input("Enter user: ")
        self.password = input("Enter password: ")


class TokenManager:

    def __init__(self, credential_manager):
        print("Initializing token manager")
        self.cm = credential_manager
        if not self.cm.user or not self.cm.password:
            raise Exception("Credentials not entered")
        _data = {
            "username": self.cm.user,
            "password": self.cm.password,
            "grant_type": "password"
        }
        print("Getting token")
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
        api_url = f'{api_base_url}/token'
        response = r.post(api_url, data=_data)
        if response.status_code == 200:
            self.last = time.time()
            self.token_data = response.json()
        else:
            raise Exception("Error getting token " + str(response.status_code))


def get_portfolio(token, country):
    api_url = f'{api_base_url}/api/v2/portafolio/{country}'
    return r.get(api_url, headers={"Authorization": f'Bearer {token}'}).json()


def main():
    print("IOL Trader")
    tm = TokenManager(CredentialManager())
    last_check = 0
    times = 0
    while True:
        if time.time() - last_check > 600:
            data = get_portfolio(tm.get_token(), "argentina")
            print(data)
            times = times + 1
            last_check = time.time()
        if times == 3:
            exit(0)
        time.sleep(30)
        print("Checking data")


if __name__ == '__main__':
    main()
