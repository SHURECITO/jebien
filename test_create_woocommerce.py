from woocommerce_api import create_woocommerce_product

# Datos simulados de un producto de MercadoLibre
product = {
    "title": "Producto de Prueba desde API",
    "price": 150.0,
    "inventory": 10,
    "images": ["https://www.w3schools.com/w3images/lights.jpg"],  # Imagen accesible
    "id": "ML1234567890"  # SKU basado en MercadoLibre
}

create_woocommerce_product(product)
