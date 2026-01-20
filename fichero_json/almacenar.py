import json
import os

def almacenar_json (catalogo, nombre_fichero):
    #Guarda el catalogo en un archivo JSON
    if not nombre_fichero.endswith(".json"):
        nombre_fichero += ".json"
    
    #como un 'set' no es serializable en JSON
    #lo convertimos a 'list
    datos_exportar = []

    for juego in catalogo.values():
        #convertir 'set' a 'list' para permitir la exportacion
        item = {
            "titulo": juego["titulo"],
            "anio": juego["anio"],
            "generos": list(juego["generos"])
        }
        datos_exportar.append(item)
    try:
        with open(nombre_fichero, "w", encoding="UTF-8") as fichero:
            json.dump(
                datos_exportar,
                fichero,
                ensure_ascii = False, 
                indent=4)
        print(f"\nArchivo '{nombre_fichero}' guardado correctamente")
    except Exception as exc:
        #capturar errores de E/S usando strerror
        print(f"ERROR al guardar JSON : {os.strerror(exc.errno)}")