import requests

WOOCOMMERCE_URL = "https://jebien.com"
WOOCOMMERCE_CONSUMER_KEY = "ck_5d6242d3aec9393ead16ce95b3867fc7d39b0560"
WOOCOMMERCE_CONSUMER_SECRET = "cs_f3d431071808be2f52aadd9c1b4dbd3cbb551220"

def get_woocommerce_products():
    """
    Obtiene productos desde WooCommerce.
    """
    try:
        url = f"{WOOCOMMERCE_URL}/wp-json/wc/v3/products"
        response = requests.get(url, auth=(WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET))

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al obtener productos de WooCommerce: {response.status_code}")
            return []
    except Exception as e:
        print(f"Excepción al conectarse a WooCommerce: {e}")
        return []

def create_woocommerce_product(product):
    """
    Crea un producto en WooCommerce.
    """
    try:
        url = f"{WOOCOMMERCE_URL}/wp-json/wc/v3/products"
        data = {
            "name": product["title"],
            "regular_price": str(product["price"]),
            "sku": product["id"],
            "stock_quantity": product["inventory"],
            "manage_stock": True,
            "images": [{"src": img} for img in product["images"]]
        }
        response = requests.post(url, json=data, auth=(WOOCOMMERCE_CONSUMER_KEY, WOOCOMMERCE_CONSUMER_SECRET))

        if response.status_code == 201:
            print(f"Producto creado: {product['title']}")
        else:
            print(f"Error creando producto {product['title']}: {response.json()}")
    except Exception as e:
        print(f"Excepción al crear producto {product['title']}: {e}")
