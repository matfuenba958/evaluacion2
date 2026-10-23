import requests
import urllib.parse

llave = "169705d2-ba75-4f36-b847-c646f2a10992"
url_geo = "https://graphhopper.com/api/1/geocode?"
url_ruta = "https://graphhopper.com/api/1/route?"

while True:
    print("\n--- Planificador de Rutas Biblioteca Nacional ---")
    origen = input("Ingrese la ciudad de origen (o escriba 's' o 'salir' para terminar): ")
    if origen.lower() in ['s', 'salir']:
        print("Saliendo del programa. ¡Hasta luego!")
        break

    destino = input("Ingrese la ciudad de destino (o escriba 's' o 'salir' para terminar): ")
    if destino.lower() in ['s', 'salir']:
        print("Saliendo del programa. ¡Hasta luego!")
        break

    geo_origen = requests.get(url_geo + urllib.parse.urlencode({"q": origen, "limit": "1", "key": llave})).json()
    geo_destino = requests.get(url_geo + urllib.parse.urlencode({"q": destino, "limit": "1", "key": llave})).json()

    if geo_origen.get("hits") and geo_destino.get("hits"):
        lat_origen = geo_origen["hits"][0]["point"]["lat"]
        lng_origen = geo_origen["hits"][0]["point"]["lng"]
        lat_destino = geo_destino["hits"][0]["point"]["lat"]
        lng_destino = geo_destino["hits"][0]["point"]["lng"]

        # locale=es para las instrucciones en español
        parametros_ruta = {
            "point": [f"{lat_origen},{lng_origen}", f"{lat_destino},{lng_destino}"],
            "vehicle": "car",
            "locale": "es",
            "key": llave
        }

        url_final = url_ruta + urllib.parse.urlencode(parametros_ruta, doseq=True)
        datos_ruta = requests.get(url_final).json()

        if "paths" in datos_ruta:
            ruta = datos_ruta["paths"][0]
            distancia_km = ruta["distance"] / 1000
            tiempo_min = ruta["time"] / 60000

            print(f"\nResumen del viaje:")
            # Formato de 2 decimales
            print(f"Distancia: {distancia_km:.2f} km")
            print(f"Tiempo estimado: {tiempo_min:.2f} minutos")

            print("\nInstrucciones paso a paso:")
            for instruccion in ruta["instructions"]:
                dist_paso = instruccion['distance'] / 1000
                print(f"- {instruccion['text']} ({dist_paso:.2f} km)")
        else:
            print("No se encontró ruta para estas ciudades.")
    else:
        print("No se encontraron las coordenadas de las ciudades ingresadas.")