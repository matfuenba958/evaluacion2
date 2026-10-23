import requests
import random
import string

url = "http://localhost:3000/libros"

def generar_texto(largo):
    letras = string.ascii_lowercase
    return ''.join(random.choice(letras) for i in range(largo))

def generar_isbn():
    numeros = string.digits
    return ''.join(random.choice(numeros) for i in range(9))

print("Agregando 50 libros al catálogo...")

# El id empieza desde el 8 ya que ocupamos hasta el 7
for i in range(8, 58):
    libro = {
        "id": i,
        "titulo": f"Libro {generar_texto(6)}",
        "autor": f"Autor {generar_texto(5)}",
        "isbn": generar_isbn()
    }
    requests.post(url, json=libro)

print("Libros creados. Listando los ultimos 5 para verificar:")
respuesta = requests.get(url)
if respuesta.status_code == 200:
    libros = respuesta.json()
    for lib in libros[-5:]: # Mostramos solo los ultimos 5 para que quepa en la foto
        print(lib)