"""gestor/catalogo_videojuegos.py

Módulo unificado para la gestión del catálogo de videojuegos.
Incluye tanto la lógica de negocio como el acceso a datos.
"""

from .utilidades import normalizar_titulo, normalizar_generos


def crear_catalogo():
    """Crea y devuelve un catálogo vacío."""
    return {}


def _clave(titulo):
    """Devuelve la clave interna para un título (normalizado y minúsculas)."""
    return normalizar_titulo(titulo).lower()


def crear_juego(catalogo, titulo, anio, generos):
    """Crea un nuevo videojuego en el catálogo."""
    titulo_norm = normalizar_titulo(titulo)
    generos_set = normalizar_generos(generos)

    if anio < 0:
        raise ValueError("El año no puede ser negativo.")

    clave = _clave(titulo_norm)
    if clave in catalogo:
        raise ValueError("El videojuego ya existe.")

    juego = {
        "titulo": titulo_norm,
        "anio": anio,
        "generos": generos_set,
    }
    catalogo[clave] = juego
    return juego


def obtener_juego(catalogo, titulo):
    """Devuelve el videojuego con ese título o None si no existe."""
    return catalogo.get(_clave(titulo))


def actualizar_juego(catalogo, titulo_original, nuevo_titulo=None, nuevo_anio=None, nuevos_generos=None):
    """Actualiza los datos de un videojuego existente."""
    clave_original = _clave(titulo_original)
    if clave_original not in catalogo:
        raise KeyError("No existe ese videojuego.")

    juego = catalogo[clave_original]

    # Determinar nuevos valores
    titulo_final = normalizar_titulo(nuevo_titulo) if nuevo_titulo else juego["titulo"]
    anio_final = nuevo_anio if nuevo_anio is not None else juego["anio"]
    generos_final = normalizar_generos(nuevos_generos) if nuevos_generos is not None else juego["generos"]

    if anio_final < 0:
        raise ValueError("El año no puede ser negativo.")

    # Si cambia el título, hay que cambiar la clave
    if titulo_final != juego["titulo"]:
        nueva_clave = _clave(titulo_final)
        if nueva_clave in catalogo:
             raise ValueError("Ya existe un videojuego con el nuevo título.")
        del catalogo[clave_original]
        catalogo[nueva_clave] = juego
    
    # Actualizamos el objeto juego
    juego["titulo"] = titulo_final
    juego["anio"] = anio_final
    juego["generos"] = generos_final
    
    return juego


def eliminar_juego(catalogo, titulo):
    """Elimina un videojuego del catálogo."""
    clave = _clave(titulo)
    if clave in catalogo:
        del catalogo[clave]
        return True
    return False


def listar_juegos(catalogo):
    """Devuelve una lista con todos los videojuegos del catálogo."""
    return list(catalogo.values())


def buscar_juegos_parcial(catalogo, fragmento):
    """Busca videojuegos cuyo título contenga el fragmento indicado."""
    fragmento = fragmento.strip().lower()
    return [j for j in catalogo.values() if fragmento in j["titulo"].lower()]


def buscar_juegos_por_genero(catalogo, genero):
    """Busca videojuegos que contengan el género indicado."""
    genero = genero.strip().lower()
    return [j for j in catalogo.values() if genero in j["generos"]]


def buscar_juegos_por_rango(catalogo, anio_min, anio_max):
    """Busca videojuegos cuyo año esté dentro del rango [anio_min, anio_max]."""
    if anio_min > anio_max:
        raise ValueError("El año mínimo no puede ser mayor que el año máximo.")
    return [j for j in catalogo.values() if anio_min <= j["anio"] <= anio_max]


def obtener_estadisticas(catalogo):
    """Calcula estadísticas sencillas del catálogo."""
    total = len(catalogo)
    conteo = {}
    for juego in catalogo.values():
        for genero in juego["generos"]:
            conteo[genero] = conteo.get(genero, 0) + 1
    return {"total": total, "generos": conteo}

