from woocommerce_api import update_woocommerce_stock

# SKU del producto en WooCommerce
sku = "ML1234567890"  # Cambiá por un SKU existente
stock = 0  # Nuevo stock que querés asignar

update_woocommerce_stock(sku, stock)
