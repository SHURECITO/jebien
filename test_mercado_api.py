from mercado_api import get_access_token, get_mercadolibre_products

access_token = get_access_token()
products = get_mercadolibre_products(access_token)
print(f"Productos obtenidos: {len(products)}")
for product in products[:5]:  # Muestra solo los primeros 5 productos
    print(product)
