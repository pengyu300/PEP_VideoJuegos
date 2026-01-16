"""catalogo/utilidades.py

Funciones auxiliares que se usan en varias partes del programa.

En este módulo NO hay acceso a teclado ni a pantalla.
Solo hay lógica reutilizable.
"""


def normalizar_titulo(titulo):
    """Quita espacios al principio y al final del título.

    Más adelante podrías añadir aquí más reglas de normalización
    (por ejemplo, reemplazar dobles espacios, etc.).
    """
    return titulo.strip()


def normalizar_generos(lista):
    """Recibe una lista de cadenas y devuelve un conjunto (set) de géneros.

    - Elimina espacios en blanco al principio y al final.
    - Pasa todo a minúsculas.
    - Elimina elementos vacíos.

    Ejemplo:
        [" Acción ", "rpg", "accion", ""] -> {"acción", "rpg"}
    """
    generos = set()
    for elemento in lista:
        texto = elemento.strip().lower()
        if texto:
            generos.add(texto)
    return generos
