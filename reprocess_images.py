import os
import requests
from io import BytesIO
from PIL import Image

# Credenciales WooCommerce
WOOCOMMERCE_URL = ""
CONSUMER_KEY = ""
CONSUMER_SECRET = ""

# Directorio temporal para guardar imágenes procesadas
TEMP_DIR = "temp_images"
os.makedirs(TEMP_DIR, exist_ok=True)

def get_products():
    """
    Obtiene los productos de WooCommerce con sus imágenes.
    """
    try:
        products = []
        page = 1
        while True:
            response = requests.get(
                WOOCOMMERCE_URL,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                params={"per_page": 100, "page": page}
            )
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break  # No hay más productos
                products.extend(data)
                page += 1
            else:
                print(f"Error al obtener productos: {response.status_code}")
                print(response.json())
                break
        return products
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []

def process_image(image_url, output_size=(800, 800)):
    """
    Descarga y reescala una imagen desde una URL.
    """
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image = image.resize(output_size, Image.LANCZOS)
            return image
        else:
            print(f"No se pudo descargar la imagen desde {image_url}. Código: {response.status_code}")
    except Exception as e:
        print(f"Error al procesar la imagen: {e}")
    return None

def upload_image_to_woocommerce(product_id, image_path, image_index):
    """
    Sube una nueva imagen procesada a WooCommerce mediante el endpoint del producto.
    """
    try:
        with open(image_path, "rb") as img_file:
            # Subir la imagen como archivo binario al servidor
            files = {
                "file": (os.path.basename(image_path), img_file, "image/jpeg"),
            }
            media_upload_url = f"{WOOCOMMERCE_URL}/media"
            response = requests.post(
                media_upload_url,
                auth=(CONSUMER_KEY, CONSUMER_SECRET),
                files=files
            )

            if response.status_code == 201:
                uploaded_image = response.json()
                print(f"Imagen {image_index + 1} subida exitosamente para el producto ID: {product_id}")
                return uploaded_image["id"]
            else:
                print(f"Error al subir imagen {image_index + 1} para el producto ID: {product_id}")
                print(response.json())
                return None
    except Exception as e:
        print(f"Error al subir imagen {image_index + 1} para el producto ID: {product_id}: {e}")
        return None


def reprocess_product_images():
    """
    Reescala todas las imágenes de los productos en WooCommerce.
    """
    products = get_products()
    if not products:
        print("No se encontraron productos en WooCommerce.")
        return

    for product in products:
        if not product.get("images"):
            print(f"El producto ID {product['id']} no tiene imágenes. Se omite.")
            continue  # Saltar productos sin imágenes

        product_id = product["id"]
        print(f"\nProcesando imágenes del producto ID: {product_id}")

        updated_images = []
        for index, image_data in enumerate(product["images"]):
            original_image_url = image_data["src"]
            print(f" - Procesando imagen {index + 1}: {original_image_url}")

            # Descargar y procesar la imagen
            image = process_image(original_image_url)
            if image:
                # Guardar la imagen procesada en un archivo temporal
                temp_image_path = os.path.join(TEMP_DIR, f"{product_id}_{index}.jpg")
                try:
                    image.save(temp_image_path, "JPEG")

                    # Subir la imagen procesada a WooCommerce y obtener su ID
                    uploaded_image_id = upload_image_to_woocommerce(product_id, temp_image_path, index)
                    if uploaded_image_id:
                        updated_images.append({"id": uploaded_image_id})
                finally:
                    # Eliminar el archivo temporal
                    if os.path.exists(temp_image_path):
                        os.remove(temp_image_path)
            else:
                print(f" - Error al procesar la imagen {index + 1} del producto ID: {product_id}")

        # Actualizar las imágenes del producto en WooCommerce
        if updated_images:
            update_url = f"{WOOCOMMERCE_URL}/{product_id}"
            try:
                response = requests.put(
                    update_url,
                    auth=(CONSUMER_KEY, CONSUMER_SECRET),
                    json={"images": updated_images}
                )
                if response.status_code == 200:
                    print(f"Imágenes actualizadas para el producto ID: {product_id}")
                else:
                    print(f"Error al actualizar imágenes del producto ID: {product_id}")
                    print(response.json())
            except Exception as e:
                print(f"Error crítico al actualizar imágenes del producto ID: {product_id}: {e}")


if __name__ == "__main__":
    try:
        reprocess_product_images()
    except Exception as e:
        print(f"Error crítico en la ejecución: {e}")
