import requests

# Credenciales de WooCommerce
WOOCOMMERCE_URL = "https://jebien.com/wp-json/wc/v3/products"  # Cambiá por la URL de tu tienda
CONSUMER_KEY = "ck_5d6242d3aec9393ead16ce95b3867fc7d39b0560"  # Reemplazá con tu Consumer Key
CONSUMER_SECRET = "cs_f3d431071808be2f52aadd9c1b4dbd3cbb551220"  # Reemplazá con tu Consumer Secret


def get_woocommerce_products():
    """
    Obtiene todos los productos desde WooCommerce con soporte para paginación.
    """
    products = []
    page = 1  # Empezamos en la página 1
    per_page = 100  # Límite máximo por solicitud (100 productos)

    try:
        while True:
            # Solicitar productos con paginación
            response = requests.get(
                WOOCOMMERCE_URL,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                params={"per_page": per_page, "page": page},
            )
            if response.status_code == 200:
                page_products = response.json()
                if not page_products:
                    break  # Salir si no hay más productos

                # Procesar productos obtenidos
                for product in page_products:
                    products.append({
                        "id": product["id"],
                        "sku": product.get("sku", ""),  # Validar que exista el campo SKU
                        "stock_quantity": product.get("stock_quantity", 0),  # Asegurar stock válido
                    })
                print(f"Página {page}: {len(page_products)} productos obtenidos.")
                page += 1  # Ir a la siguiente página
            else:
                print(f"Error al obtener productos de WooCommerce: {response.status_code}")
                print(response.text)
                break
    except Exception as e:
        print(f"Excepción al obtener productos de WooCommerce: {e}")

    return products



def create_woocommerce_product(product):
    """
    Crea un producto en WooCommerce con los datos de MercadoLibre.
    """
    headers = {"Content-Type": "application/json"}

    # Ajustar el stock según el inventario de MercadoLibre
    stock = max(0, product["inventory"] - 2)  # Restamos 2 unidades según la lógica del negocio

    # Validar imágenes
    images = [{"src": img} for img in product["images"] if img.startswith("http")]

    # Preparar los datos del producto
    data = {
        "name": product["title"],
        "type": "simple",
        "regular_price": str(product["price"]),
        "stock_quantity": stock,
        "manage_stock": True,
        "in_stock": stock > 0,  # Si el stock es 0, WooCommerce marcará el producto como "Sin Stock"
        "images": images,  # Solo incluir imágenes válidas
        "sku": product["id"],  # ID de MercadoLibre como SKU
    }

    try:
        response = requests.post(WOOCOMMERCE_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET), headers=headers, json=data)
        if response.status_code == 201:
            print(f"Producto creado en WooCommerce: {product['title']}")
        else:
            print(f"Error al crear producto en WooCommerce: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Excepción al crear producto en WooCommerce: {e}")



def update_woocommerce_stock(sku, stock):
    """
    Actualiza el inventario de un producto en WooCommerce.
    """
    headers = {"Content-Type": "application/json"}

    # Buscar producto por SKU
    try:
        search_response = requests.get(WOOCOMMERCE_URL, auth=(CONSUMER_KEY, CONSUMER_SECRET), params={"sku": sku})
        if search_response.status_code == 200 and search_response.json():
            product_id = search_response.json()[0]["id"]  # Obtener el ID del producto
            update_url = f"{WOOCOMMERCE_URL}/{product_id}"

            # Actualizar stock
            data = {
                "stock_quantity": stock,
                "in_stock": stock > 0  # Marcar como "Sin Stock" si el stock es 0
            }
            update_response = requests.put(update_url, auth=(CONSUMER_KEY, CONSUMER_SECRET), headers=headers, json=data)
            if update_response.status_code == 200:
                print(f"Inventario actualizado para el producto SKU: {sku}, Stock: {stock}")
            else:
                print(f"Error al actualizar stock en WooCommerce: {update_response.status_code}")
                print(update_response.text)
        else:
            print(f"No se encontró producto en WooCommerce con SKU: {sku}")
    except Exception as e:
        print(f"Excepción al actualizar inventario en WooCommerce: {e}")
