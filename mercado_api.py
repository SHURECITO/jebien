import requests
import json
import time

# Credenciales de tu aplicación en MercadoLibre
CLIENT_ID = "1285162163304558"  # Reemplaza con tu APP_ID
CLIENT_SECRET = "4xfMTIMOTtdB8gvmOw4QlTyWzzFawgBS"  # Reemplaza con tu SECRET_KEY
REDIRECT_URI = "https://jebien.com/"  # Debe coincidir con el configurado en tu app

# Archivo donde se guardarán los tokens
TOKEN_FILE = "tokens.json"

def save_token_to_file(token_info):
    """
    Guarda los tokens en un archivo JSON.
    """
    try:
        with open("tokens.json", "w") as file:
            json.dump(token_info, file)
        print("Tokens guardados exitosamente.")
    except Exception as e:
        print(f"Error al guardar tokens: {e}")

def load_token_from_file():
    """
    Carga los tokens desde un archivo JSON.
    """
    try:
        with open(TOKEN_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("No se encontró el archivo de tokens.")
        return None
    except Exception as e:
        print(f"Error al cargar tokens: {e}")
        return None

def generate_access_token(auth_code):
    """
    Genera un token de acceso inicial usando el Authorization Code.
    """
    url = "https://api.mercadolibre.com/oauth/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            save_token_to_file(token_info)
            print("Token de acceso generado exitosamente.")
            return token_info
        else:
            print(f"Error al generar token: {response.status_code}")
            print(f"Detalle: {response.text}")
    except Exception as e:
        print(f"Excepción al generar token: {e}")
        return None

def refresh_access_token():
    """
    Renueva el token de acceso usando el Refresh Token.
    """
    token_info = load_token_from_file()
    if not token_info or "refresh_token" not in token_info:
        print("No se encontró un Refresh Token válido.")
        return None

    url = "https://api.mercadolibre.com/oauth/token"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": token_info["refresh_token"],
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            new_token_info = response.json()
            save_token_to_file(new_token_info)
            print("Token renovado exitosamente.")
            return new_token_info
        else:
            print(f"Error al renovar token: {response.status_code}")
            print(f"Detalle: {response.text}")
    except Exception as e:
        print(f"Excepción al renovar token: {e}")
        return None

def get_access_token():
    """
    Obtiene el token de acceso válido, renovándolo si es necesario.
    """
    token_info = load_token_from_file()
    if token_info and "access_token" in token_info:
        return token_info["access_token"]

    print("El token de acceso no es válido o no existe. Intenta generar uno nuevo.")
    return None

def get_mercadolibre_products():
    """
    Obtiene todos los productos desde la API de MercadoLibre usando el UserID.
    """
    access_token = get_access_token()
    if not access_token:
        print("No se pudo obtener un token válido.")
        return []

    # Obtener información del usuario
    user_info_url = f"https://api.mercadolibre.com/users/me?access_token={access_token}"
    try:
        user_response = requests.get(user_info_url)
        if user_response.status_code != 200:
            print(f"Error al obtener información del usuario: {user_response.status_code}")
            print(user_response.text)
            return []

        user_id = user_response.json().get("id")
        if not user_id:
            print("No se pudo obtener el UserID del usuario.")
            return []
    except Exception as e:
        print(f"Excepción al obtener el UserID del usuario: {e}")
        return []

    # Obtener productos del usuario con paginación
    products = []
    offset = 0
    limit = 50

    while True:
        products_url = f"https://api.mercadolibre.com/users/{user_id}/items/search"
        try:
            response = requests.get(products_url, params={"access_token": access_token, "limit": limit, "offset": offset})
            if response.status_code == 200:
                data = response.json()
                product_ids = data.get('results', [])
                total_products = data.get('paging', {}).get('total', 0)

                if not product_ids:
                    break  # No hay más productos para procesar

                print(f"Obteniendo productos {offset + 1} a {offset + len(product_ids)} de {total_products}...")
                
                # Obtener detalles de cada producto
                for product_id in product_ids:
                    try:
                        product_details_url = f"https://api.mercadolibre.com/items/{product_id}?access_token={access_token}"
                        product_response = requests.get(product_details_url)

                        if product_response.status_code == 200:
                            product_data = product_response.json()
                            products.append({
                                "id": product_data["id"],
                                "title": product_data["title"],
                                "price": product_data["price"],
                                "inventory": product_data["available_quantity"],
                                "images": [img["url"] for img in product_data["pictures"]]
                            })
                        else:
                            print(f"Error al obtener detalles del producto {product_id}: {product_response.status_code}")
                    except Exception as e:
                        print(f"Error al procesar producto {product_id}: {e}")

                # Incrementar el offset para la siguiente página
                offset += limit

                # Salir si hemos procesado todos los productos
                if offset >= total_products:
                    break

                # Retardo para evitar exceder el límite de la API
                time.sleep(1)  # Ajustá según los límites de la API
            else:
                print(f"Error al obtener productos: {response.status_code}")
                print(response.text)
                break
        except Exception as e:
            print(f"Excepción general al conectarse a MercadoLibre: {e}")
            break

    return products
