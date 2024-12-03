import pandas as pd

def generate_excel_report(mercado_products, woocommerce_products, non_linked_products):
    """
    Genera un reporte en Excel.
    """
    try:
        resumen = {
            "Total MercadoLibre": [len(mercado_products)],
            "Total WooCommerce": [len(woocommerce_products)],
            "No Enlazados": [len(non_linked_products)]
        }

        resumen_df = pd.DataFrame(resumen)
        no_enlazados_df = pd.DataFrame(non_linked_products)

        with pd.ExcelWriter("reporte_productos.xlsx") as writer:
            resumen_df.to_excel(writer, sheet_name="Resumen", index=False)
            no_enlazados_df.to_excel(writer, sheet_name="No Enlazados", index=False)

        print("Reporte generado: reporte_productos.xlsx")
    except Exception as e:
        print(f"Error al generar reporte: {e}")
