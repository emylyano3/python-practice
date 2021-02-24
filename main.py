import requests as r


api_base_url = "https://api.invertironline.com"


class CredentialManager:

    def __init__(self):
        self.user = input("Ingrese el usuario: ")
        self.password = input("Ingrese la contraseña: ")


class TokenManager:

    def __init__(self, credential_manager):
        self.cm = credential_manager
        self.access_token = ""
        self.refresh_token = ""
        self.__get_access_token()

    def get_token(self):
        return self.access_token

    def __get_access_token(self):
        if not self.cm.user or not self.cm.password:
            raise Exception("Credenciales no ingresadas")
        post_data = {
            "username": self.cm.user,
            "password": self.cm.password,
            "grant_type": "password"
        }
        api_url = f'{api_base_url}/token'
        response = r.post(api_url, data=post_data)
        if response.status_code == 200:
            response_data = response.json()
            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]
        else:
            self.access_token = ""
            self.refresh_token = ""
            raise Exception("Error obteniendo el token " + str(response.status_code))

    def __get_token_refreshed(self):
        if not self.refresh_token:
            raise Exception("No existe token para renovar. Ejecutar primero el metodo get_access_token.")
        post_data = {
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        api_url = f'{api_base_url}/token'
        response = r.post(api_url, data=post_data)
        if response.status_code == 200:
            response_data = response.json()
            self.access_token = response_data["access_token"]
            self.refresh_token = response_data["refresh_token"]
        else:
            self.access_token = ""
            self.refresh_token = ""
            raise Exception("Error obteniendo el token " + str(response.status_code))


def get_portfolio(token, country):
    api_url = f'{api_base_url}/api/v2/portafolio/{country}'
    return r.get(api_url, headers={"Authorization": f'Bearer {token}'}).json()


def main():
    print("IOL Trader")
    tm = TokenManager(CredentialManager())
    data = get_portfolio(tm.get_token(), "argentina")
    print(data)


if __name__ == '__main__':
    main()
