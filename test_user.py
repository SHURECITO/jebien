import requests

def test_user_info(access_token):
    url = f"https://api.mercadolibre.com/users/me?access_token={access_token}"
    response = requests.get(url)
    if response.status_code == 200:
        print("Usuario asociado al token:")
        print(response.json())
    else:
        print(f"Error al obtener información del usuario: {response.status_code}")
        print(response.text)

# Probá con el token actual
from mercado_api import get_access_token
access_token = get_access_token()
test_user_info(access_token)
