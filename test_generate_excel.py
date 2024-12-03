from excel_report import generate_excel_report

mercado_products = [
    {"id": "ML1234567890", "title": "Producto A", "price": 150.0, "inventory": 10},
    {"id": "ML0987654321", "title": "Producto B", "price": 200.0, "inventory": 5},
]

woocommerce_products = [
    {"sku": "ML1234567890", "stock_quantity": 8},
]

generate_excel_report(mercado_products, woocommerce_products)
