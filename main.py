import requests as r

access_token = ""
refresh_token = ""
user = ""
password = ""
api_base_url = "https://api.invertironline.com"


def get_access_token():
    global user, password, access_token, refresh_token
    if not user or not password:
        raise Exception("Credenciales no ingresadas")
    post_data = {
        "username": user,
        "password": password,
        "grant_type": "password"
    }
    api_url = f'{api_base_url}/token'
    response = r.post(api_url, data=post_data)
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
    else:
        access_token = ""
        refresh_token = ""
        raise Exception("Error obteniendo el token " + str(response.status_code))


def get_token_refreshed():
    global access_token, refresh_token
    if not refresh_token or not access_token:
        raise Exception("No existe token para renovar. Ejecutar primero el metodo getToken.")
    post_data = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    api_url = f'{api_base_url}/token'
    response = r.post(api_url, data=post_data)
    if response.status_code == 200:
        response_data = response.json()
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
    else:
        access_token = ""
        refresh_token = ""
        raise Exception("Error obteniendo el token " + str(response.status_code))


def get_credentials():
    global user, password
    user = input("Ingrese el usuario: ")
    password = input("Ingrese la contraseña: ")


def get_portfolio():
    api_url = f'{api_base_url}/api/v2/portafolio/argentina'
    data = r.get(api_url, headers={"Authorization": f'Bearer {access_token}'})
    print(data.json())


def main():
    print("IOL Trader")
    get_credentials()
    get_access_token()
    get_portfolio()


if __name__ == '__main__':
    main()
