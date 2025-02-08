from mercado_api import regenerate_access_token

def test_regenerate_token():
    """
    Prueba la regeneración del token de acceso desde MercadoLibre.
    """
    try:
        # Llamar a la función para regenerar el token
        new_token = regenerate_access_token()
        
        if new_token:
            print(f"Nuevo token generado exitosamente: {new_token}")
        else:
            print("No se pudo generar un nuevo token. Verifica las credenciales o la configuración.")
    
    except Exception as e:
        print(f"Error al regenerar el token: {e}")

# Ejecutar la prueba
test_regenerate_token()
