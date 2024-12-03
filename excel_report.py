import openpyxl

def generate_excel_report(mercado_products, woocommerce_products):
    """
    Genera un reporte en Excel con productos de MercadoLibre y WooCommerce.
    """
    try:
        # Crear un libro de Excel
        workbook = openpyxl.Workbook()
        summary_sheet = workbook.active
        summary_sheet.title = "Resumen"

        # Hoja 1: Resumen General
        summary_sheet.append(["Cantidad Total de Productos en MercadoLibre", len(mercado_products)])
        summary_sheet.append(["Cantidad Total de Productos en WooCommerce", len(woocommerce_products)])
        summary_sheet.append([
            "Cantidad de Productos No Enlazados",
            len([p for p in mercado_products if p["id"] not in {w["sku"] for w in woocommerce_products}])
        ])

        # Hoja 2: Detalles de Productos No Enlazados
        details_sheet = workbook.create_sheet(title="No Enlazados")
        details_sheet.append(["Título", "ID (MercadoLibre)", "Precio", "Inventario"])
        no_enlazados = [
            p for p in mercado_products if p["id"] not in {w["sku"] for w in woocommerce_products}
        ]
        for product in no_enlazados:
            details_sheet.append([
                product["title"],
                product["id"],
                product["price"],
                product["inventory"]
            ])

        # Guardar el archivo Excel
        workbook.save("reporte_productos.xlsx")
        print("Reporte generado exitosamente: reporte_productos.xlsx")

    except Exception as e:
        print(f"Error al generar el reporte en Excel: {e}")
