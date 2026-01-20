"""catalogo/menu.py

Módulo con la INTERFAZ DE USUARIO por consola (línea de comandos).

Aquí sí usamos:
    - input() para leer del teclado.
    - print() para mostrar información al usuario.

Este módulo NO contiene la lógica de negocio ni sabe cómo se guardan
los datos por dentro. Cuando hay que hacer algo con el catálogo,
llamamos a las funciones de catalogo_videojuegos.py.
"""

import os
from . import catalogo_videojuegos
from fichero_json import almacenar as json_alm
from fichero_json import leer as json_leer


def mostrar_videojuego(juego):
    """Muestra por pantalla la información de un videojuego.

    Esta función solo se encarga de la presentación.
    """
    print("Título:", juego["titulo"])
    print("Año:", juego["anio"])
    print("Géneros:", ", ".join(sorted(juego["generos"])))
    print("-" * 40)


def pedir_datos_videojuego():
    """Pide al usuario los datos básicos de un videojuego.

    Devuelve:
        (titulo, anio, lista_generos)

    Si el usuario escribe un año no numérico, se producirá una excepción
    ValueError que se gestionará en el menú principal.
    """
    titulo = input("Título: ")
    anio_texto = input("Año: ")
    anio = int(anio_texto)

    generos_texto = input("Géneros (separados por comas): ")
    if generos_texto.strip():
        lista_generos = generos_texto.split(",")
    else:
        lista_generos = []

    return titulo, anio, lista_generos


def mostrar_menu():
    """Muestra el menú de opciones por pantalla."""
    print("\n===== CATÁLOGO DE VIDEOJUEGOS =====")
    print("1. Listar videojuegos")
    print("2. Añadir videojuego")
    print("3. Consultar videojuego por título")
    print("4. Actualizar videojuego")
    print("5. Eliminar videojuego")
    print("6. Buscar por título (parcial)")
    print("7. Buscar por género")
    print("8. Buscar por rango de años")
    print("9. Mostrar estadísticas")

    #añadir opciones de los ficheros 
    print("10. Guardar catalogo en CSV")
    print("11. Cargar catalogo desde CSV")
    print("12. Guardar catalogo en JSON")
    print("13. Cargar catalogo desde JSON")

    print("0. Salir")
    print("===================================")


def menu_principal():
    """Bucle principal del programa.

    Aquí se crea el catálogo en memoria y se llama a las funciones
    del gestor unificado según la opción elegida.
    """
    videojuegos = catalogo_videojuegos.crear_catalogo()

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ").strip()
        print()

        try:
            if opcion == "1":
                # Listar todos los videojuegos
                videojuegos_lista = catalogo_videojuegos.listar_juegos(videojuegos)
                if not videojuegos_lista:
                    print("\nNo hay videojuegos en el catálogo.\n")
                else:
                    print()
                    for juego in videojuegos_lista:
                        mostrar_videojuego(juego)

            elif opcion == "2":
                # Añadir nuevo videojuego
                titulo, anio, generos = pedir_datos_videojuego()
                juego = catalogo_videojuegos.crear_juego(videojuegos, titulo, anio, generos)
                print("\nVideojuego añadido correctamente.\n")
                mostrar_videojuego(juego)

            elif opcion == "3":
                # Consultar por título
                titulo = input("Título a buscar: ")
                juego = catalogo_videojuegos.obtener_juego(videojuegos, titulo)
                if juego is None:
                    print("\nNo se encontró el videojuego.\n")
                else:
                    mostrar_videojuego(juego)

            elif opcion == "4":
                # Actualizar videojuego
                titulo_original = input("Título del videojuego a actualizar: ")
                print("Deja en blanco para mantener el valor actual.")

                nuevo_titulo = input("Nuevo título: ").strip()
                if not nuevo_titulo:
                    nuevo_titulo = None

                nuevo_anio_texto = input("Nuevo año: ").strip()
                if nuevo_anio_texto:
                    nuevo_anio = int(nuevo_anio_texto)
                else:
                    nuevo_anio = None

                nuevos_generos_texto = input(
                    "Nuevos géneros (separados por comas, en blanco para mantener): "
                ).strip()
                if nuevos_generos_texto:
                    nuevos_generos = nuevos_generos_texto.split(",")
                else:
                    nuevos_generos = None

                juego = catalogo_videojuegos.actualizar_juego(
                    videojuegos,
                    titulo_original,
                    nuevo_titulo,
                    nuevo_anio,
                    nuevos_generos,
                )
                print("\nVideojuego actualizado correctamente.\n")
                mostrar_videojuego(juego)

            elif opcion == "5":
                # Eliminar videojuego
                titulo = input("Título del videojuego a eliminar: ")
                borrado = catalogo_videojuegos.eliminar_juego(videojuegos, titulo)
                if borrado:
                    print("\nVideojuego eliminado.\n")
                else:
                    print("\nNo se encontró el videojuego.\n")

            elif opcion == "6":
                # Búsqueda parcial por título
                fragmento = input("Fragmento del título: ")
                resultados = catalogo_videojuegos.buscar_juegos_parcial(videojuegos, fragmento)
                if not resultados:
                    print("\nNo se encontraron videojuegos que coincidan.\n")
                else:
                    for juego in resultados:
                        mostrar_videojuego(juego)

            elif opcion == "7":
                # Búsqueda por género
                genero = input("Género a buscar: ")
                resultados = catalogo_videojuegos.buscar_juegos_por_genero(videojuegos, genero)
                if not resultados:
                    print("\nNo se encontraron videojuegos de ese género.\n")
                else:
                    for juego in resultados:
                        mostrar_videojuego(juego)

            elif opcion == "8":
                # Búsqueda por rango de años
                anio_min_texto = input("Año mínimo: ")
                anio_max_texto = input("Año máximo: ")
                anio_min = int(anio_min_texto)
                anio_max = int(anio_max_texto)

                resultados = catalogo_videojuegos.buscar_juegos_por_rango(
                    videojuegos, anio_min, anio_max
                )
                if not resultados:
                    print("\nNo se encontraron videojuegos en ese rango de años.\n")
                else:
                    for juego in resultados:
                        mostrar_videojuego(juego)

            elif opcion == "9":
                # Mostrar estadísticas
                est = catalogo_videojuegos.obtener_estadisticas(videojuegos)
                print("Número total de videojuegos:", est["total"])
                print("Conteo por género:")
                if not est["generos"]:
                    print("  (No hay géneros registrados)")
                else:
                    for genero, cantidad in sorted(est["generos"].items()):
                        print("  -", genero, ":", cantidad)

            elif opcion == "10":
                # Guardar en un fichero CSV
                videojuegos_lista = catalogo_videojuegos.listar_juegos(videojuegos)
                if not videojuegos_lista:
                    print("\nNo hay videojuegos en el catálogo.\n")
                else:
                    nombre_fichero = input("Nombre del fichero: ")
                    catalogo_videojuegos.escribir_csv(videojuegos_lista, nombre_fichero)

            elif opcion == "11":
                # Leer catalogo de un fichero CSV
                nombre_fichero = input("Nombre del fichero: ")
                catalogo_fichero = catalogo_videojuegos.leer_csv(nombre_fichero)

                videojuegos_lista = catalogo_videojuegos.listar_juegos(catalogo_fichero)
                if not videojuegos_lista:
                    print("\nNo hay videojuegos en el catálogo.\n")
                else:
                    print()
                    for juego in videojuegos_lista:
                        mostrar_videojuego(juego)
            
            elif opcion == "12":
                nombre = input("Nombre del archivo JSON para guardad : ")
                json_alm.almacenar_json(videojuegos,nombre)
            elif opcion == "13":
                nombre = input("Nombre del archivo JSON para cargar : ")
                nuevo_cat = json_leer.cargar_json(nombre)
                if nuevo_cat is not None:
                    videojuegos = nuevo_cat

            elif opcion == "0":
                # Salir del programa
                print("\nSaliendo del programa... Hasta pronto.\n")
                break
            else:
                print("\nOpción no válida. Intenta de nuevo.\n")
                
        # Errores habituales: conversión de texto a entero, etc.
        except ValueError as error:
            print("Error de datos:", error)
        except KeyError as error:
            print("Error:", error)
