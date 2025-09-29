import requests
import json

OLLAMA_URL = "http://localhost:11434/api/tags"
print(f"Intentando conectar a: {OLLAMA_URL}")

try:
    # Asegúrate de que el servicio de Ollama esté corriendo
    response = requests.get(OLLAMA_URL, timeout=5)
    print(f"Código de estado HTTP: {response.status_code}")

    if response.status_code == 200:
        print("¡Conexión exitosa!")
        print("Modelos encontrados:")
        print(json.dumps(response.json(), indent=2))
    else:
        print("Error: El servidor respondió con un código inesperado.")
        print("Respuesta:", response.text)

except requests.exceptions.RequestException as e:
    print("\n--- ERROR ---")
    print("No se pudo conectar al servidor de Ollama.")
    print("Posibles causas:")
    print("1. El servicio de Ollama no está en ejecución.")
    print("2. El Firewall de Windows está bloqueando la conexión de Python.")
    print(f"Error detallado: {e}")