from mercado_api import get_mercadolibre_products

def test_get_products():
    """
    Prueba la obtención de productos desde MercadoLibre.
    """
    try:
        products = get_mercadolibre_products()
        print(f"Productos obtenidos: {len(products)}")
        for product in products:
            print(f"{product['title']} - ID: {product['id']}")
    except Exception as e:
        print(f"Error al obtener productos: {e}")

# Ejecutar la prueba
test_get_products()
