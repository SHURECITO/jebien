from mercado_api import refresh_access_token, get_access_token, get_mercadolibre_products
from woocommerce_api import get_woocommerce_products, create_woocommerce_product
from excel_report import generate_excel_report

def main():
    try:
        # Paso 1: Renovar el token automáticamente si es necesario
        print("Validando y renovando token de MercadoLibre si es necesario...")
        refresh_access_token()

        # Paso 2: Obtener el token válido
        access_token = get_access_token()
        if not access_token:
            print("No se pudo obtener un token válido. Genera uno nuevo manualmente.")
            return

        # Paso 3: Obtener productos de MercadoLibre
        print("Obteniendo productos desde MercadoLibre...")
        mercado_products = get_mercadolibre_products()
        if not mercado_products:
            print("No se obtuvieron productos desde MercadoLibre. Revisa tu configuración.")
            return
        print(f"Productos obtenidos de MercadoLibre: {len(mercado_products)}")

        # Paso 4: Obtener productos de WooCommerce
        print("Obteniendo productos desde WooCommerce...")
        woocommerce_products = get_woocommerce_products()
        if not woocommerce_products:
            print("No se obtuvieron productos desde WooCommerce. Revisa tu configuración.")
            return
        print(f"Productos obtenidos de WooCommerce: {len(woocommerce_products)}")

        # Paso 5: Detectar productos no enlazados
        woocommerce_skus = {product["sku"] for product in woocommerce_products}
        non_linked_products = [
            product for product in mercado_products if product["id"] not in woocommerce_skus
        ]
        print(f"Productos no enlazados detectados: {len(non_linked_products)}")

        # Paso 6: Generar reporte en Excel
        print("Generando reporte en Excel...")
        generate_excel_report(mercado_products, woocommerce_products, non_linked_products)
        print("Reporte generado exitosamente: reporte_productos.xlsx")

        # Paso 7: Subir productos faltantes a WooCommerce
        print("Subiendo productos no enlazados a WooCommerce...")
        for product in non_linked_products:
            create_woocommerce_product(product)
        print("Productos no enlazados subidos exitosamente.")

    except Exception as e:
        print(f"Error en la ejecución principal: {e}")

if __name__ == "__main__":
    main()