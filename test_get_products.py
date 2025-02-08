from mercado_api import get_mercadolibre_products

def test_get_products():
    """
    Prueba la obtención de productos desde MercadoLibre.
    """
    try:
        products = get_mercadolibre_products()
        print(f"Productos obtenidos: {len(products)}")

        for index, product in enumerate(products[:5], start=1):  # Solo se muestran los primeros 5 productos para el efecto de la prueba
            print(f"{index}. {product['title']} - ID: {product['id']}")

    except Exception as e:
        print(f"Error al obtener productos: {e}")

# Ejecutar la prueba
test_get_products()
