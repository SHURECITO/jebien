from mercado_api import generate_access_token

AUTHORIZATION_CODE = ""

def main():
    print("Generando el token inicial...")
    generate_access_token(AUTHORIZATION_CODE)

if __name__ == "__main__":
    main()
