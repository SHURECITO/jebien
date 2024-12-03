from mercado_api import get_mercadolibre_products
from woocommerce_api import get_woocommerce_products, create_woocommerce_product, update_woocommerce_stock
from excel_report import generate_excel_report

def main():
    try:
        # Obtener productos de MercadoLibre
        print("Obteniendo productos de MercadoLibre...")
        mercado_products = get_mercadolibre_products()
        print(f"Productos obtenidos de MercadoLibre: {len(mercado_products)}")

        # Obtener productos de WooCommerce
        print("Obteniendo productos de WooCommerce...")
        woocommerce_products = get_woocommerce_products()
        print(f"Productos obtenidos de WooCommerce: {len(woocommerce_products)}")

        # Mapear SKUs existentes en WooCommerce
        woocommerce_skus = {p["sku"]: p for p in woocommerce_products}

        # Inicializar contadores y listas de resultados
        enlazados = []
        no_enlazados = []
        errores = []

        # Procesar productos de MercadoLibre
        for index, product in enumerate(mercado_products, start=1):
            try:
                if product["id"] in woocommerce_skus:
                    # Producto ya enlazado: Actualizar inventario
                    stock = max(0, product["inventory"] - 2)
                    update_woocommerce_stock(product["id"], stock)
                    enlazados.append(product)
                else:
                    # Producto no enlazado: Crear en WooCommerce
                    create_woocommerce_product(product)
                    no_enlazados.append(product)

            except Exception as e:
                # Registrar errores sin detener la ejecución
                errores.append({
                    "id": product["id"],
                    "title": product["title"],
                    "error": str(e),
                })

            # Reportar progreso cada 50 productos
            if index % 50 == 0:
                print(f"Progreso: {index}/{len(mercado_products)} productos procesados.")

        # Resumen final en consola
        print("\n===== Resumen Final =====")
        print(f"Productos enlazados: {len(enlazados)}")
        print(f"Productos no enlazados (creados): {len(no_enlazados)}")
        print(f"Errores encontrados: {len(errores)}")

        # Generar reporte en Excel
        print("\nGenerando reporte en Excel...")
        generate_excel_report(mercado_products, woocommerce_products)
        print("Reporte generado exitosamente: reporte_productos.xlsx")

        # Registrar errores en un archivo separado
        if errores:
            with open("errores_woocommerce.txt", "w") as error_file:
                for error in errores:
                    error_file.write(f"ID: {error['id']}, Título: {error['title']}, Error: {error['error']}\n")
            print(f"Errores registrados en 'errores_woocommerce.txt'")

    except Exception as e:
        print(f"Error crítico durante la ejecución: {e}")


if __name__ == "__main__":
    main()
