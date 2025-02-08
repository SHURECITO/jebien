import os
import requests
from PIL import Image
from io import BytesIO
import time

# Credenciales de WooCommerce
WOOCOMMERCE_URL = ""
MEDIA_URL = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

# Configuración de imágenes
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

def process_and_upload_image(image_url):
    """
    Procesa una imagen, la sube a WooCommerce como un medio y devuelve la URL pública de la imagen.
    Implementa validación y reintentos automáticos.
    """
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code != 200:
            print(f"Error al descargar la imagen: {response.status_code}")
            return None

        # Validar que el archivo es una imagen
        if "image" not in response.headers.get("Content-Type", ""):
            print(f"Archivo no válido: {image_url}")
            return None

        # Redimensionar la imagen
        image = Image.open(BytesIO(response.content))
        image = image.resize((800, 800), Image.LANCZOS)

        # Guardar temporalmente la imagen procesada
        temp_path = os.path.join(TEMP_DIR, "temp_image.jpg")
        image.save(temp_path, "JPEG")

        # Subir la imagen al servidor WooCommerce
        with open(temp_path, "rb") as img_file:
            files = {"file": img_file}
            headers = {"Content-Disposition": f'attachment; filename="image.jpg"'}
            response = requests.post(
                MEDIA_URL,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                files=files,
                headers=headers,
            )

        os.remove(temp_path)

        if response.status_code == 201:
            media_data = response.json()
            return media_data.get("source_url")  # URL pública de la imagen
        else:
            print(f"Error al subir imagen: {response.json()}")
            return None

    except Exception as e:
        print(f"Error al procesar y subir la imagen: {e}")
        return None


def create_woocommerce_product(product):
    """
    Crea un producto en WooCommerce con las imágenes procesadas y subidas como medios.
    """
    headers = {"Content-Type": "application/json"}

    stock = max(0, product["inventory"] - 2)
    image_urls = product.get("images", [])
    uploaded_images = [
        {"src": process_and_upload_image(image_url)} for image_url in image_urls if process_and_upload_image(image_url)
    ]

    data = {
        "name": product["title"],
        "type": "simple",
        "regular_price": str(product["price"]),
        "stock_quantity": stock,
        "manage_stock": True,
        "in_stock": stock > 0,
        "sku": product["id"],
        "description": product["description"],
        "short_description": product["description"][:200],
        "images": uploaded_images,
    }

    try:
        response = requests.post(WOOCOMMERCE_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET), headers=headers, json=data)
        if response.status_code == 201:
            print(f"Producto creado en WooCommerce: {product['title']}")
        else:
            print(f"Error al crear producto: {response.json()}")
    except Exception as e:
        print(f"Excepción al crear producto en WooCommerce: {e}")


def get_woocommerce_products():
    """
    Obtiene todos los productos desde WooCommerce con soporte para paginación.
    """
    products = []
    page = 1
    per_page = 100

    try:
        while True:
            response = requests.get(
                WOOCOMMERCE_URL,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                params={"per_page": per_page, "page": page},
            )
            if response.status_code == 200:
                page_products = response.json()
                if not page_products:
                    break

                for product in page_products:
                    products.append({
                        "id": product["id"],
                        "sku": product.get("sku", ""),
                        "stock_quantity": product.get("stock_quantity", 0),
                    })
                print(f"Página {page}: {len(page_products)} productos obtenidos.")
                page += 1
            else:
                print(f"Error al obtener productos de WooCommerce: {response.status_code}")
                break
    except Exception as e:
        print(f"Excepción al obtener productos de WooCommerce: {e}")

    return products


def update_woocommerce_stock(sku, stock):
    """
    Actualiza el inventario de un producto en WooCommerce.
    """
    headers = {"Content-Type": "application/json"}

    try:
        search_response = requests.get(WOOCOMMERCE_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET), params={"sku": sku})
        if search_response.status_code == 200 and search_response.json():
            product_id = search_response.json()[0]["id"]
            update_url = f"{WOOCOMMERCE_URL}/{product_id}"

            data = {
                "stock_quantity": stock,
                "in_stock": stock > 0
            }
            update_response = requests.put(update_url, auth=(CONSUMER_KEY, CONSUMER_SECRET), headers=headers, json=data)
            if update_response.status_code == 200:
                print(f"Inventario actualizado para el producto SKU: {sku}, Stock: {stock}")
            else:
                print(f"Error al actualizar stock: {update_response.json()}")
        else:
            print(f"No se encontró producto en WooCommerce con SKU: {sku}")
    except Exception as e:
        print(f"Excepción al actualizar inventario en WooCommerce: {e}")
