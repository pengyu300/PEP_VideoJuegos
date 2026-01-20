import json
import os
from gestor.utilidades import normalizar_titulo,normalizar_generos

def cargar_json(nombre_fichero):
    #lee un archivo JSON y reconstruye el catalogo
    if not nombre_fichero.endswith(".json"):
        nombre_fichero += ".json"
    nuevo_catalogo = {}

    try:
        with open(nombre_fichero, "r", encoding="UTF-8") as fichero:
            #cargar la lista de objetos desde el archivo
            lista_juegos = json.load(fichero)

            for item in lista_juegos:
                titulo = item["titulo"]
                anio = item["anio"]
                lista_generos = item["generos"]

                #convertir la lista de nuevo a un conjunto (set) de python
                generos_set = normalizar_generos(lista_generos)

                #reconstruir la clave interna (ID) para el diccionario
                clave = normalizar_titulo(titulo).lower()

                nuevo_catalogo[clave] = {
                    "titulo": normalizar_titulo(titulo),
                    "anio" : anio,
                    "generos":generos_set
                }
        print(f"\nCatalogo cargado correctamende desde '{nombre_fichero}'")
        return nuevo_catalogo
    except Exception as exc:
        #capturar errores de E/S usando strerror
        print(f"ERROR al guardar JSON : {os.strerror(exc.errno)}")
        