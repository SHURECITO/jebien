from woocommerce_api import get_woocommerce_products

products = get_woocommerce_products()
print(f"Productos obtenidos de WooCommerce: {len(products)}")
for product in products:
    print(f"SKU: {product['sku']}, Stock: {product['stock_quantity']}")
