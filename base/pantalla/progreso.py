"""Per-user lesson progress (persisted in MongoDB, per account).

Each user stores their own document in Mongo with a "progreso"
(see db.progreso_vacio). This is what allows:
  - When you register / log in, your stats start at 0.
  - When you complete a lesson, it's marked and the next one unlocks.
  - If you log out and log back in, your progress is still there.
  - If you log in with ANOTHER account, it has its own progress (zero, if it's new).
"""

from datetime import datetime, timezone
from pantalla.db import usuarios_col, obtener_usuario, progreso_vacio

# Mapa de niveles -> números de lección (debe reflejar el mismo mapa que
# usa main.py en on_abrir_leccion).
NIVELES = {
    1: [1, 2, 3, 4, 5],
    2: [1, 2, 3],
    3: [1, 2],
    4: [1, 2],
}

PUNTOS_POR_LECCION = 10


def _clave(nivel: int, num: int) -> str:
    return f"{nivel}-{num}"


def _orden_lecciones():
    orden = []
    for nivel in sorted(NIVELES):
        for num in NIVELES[nivel]:
            orden.append((nivel, num))
    return orden


def obtener_progreso(usuario: str) -> dict:
    """The user's progress, exactly as stored in the database."""
    doc = obtener_usuario(usuario) if usuario else None
    progreso = (doc or {}).get("progreso") or progreso_vacio()
    progreso.setdefault("puntos", 0)
    progreso.setdefault("racha_dias", 0)
    progreso.setdefault("lecciones", {})
    return progreso


def leccion_completada(progreso: dict, nivel: int, num: int) -> bool:
    return progreso.get("lecciones", {}).get(_clave(nivel, num), {}).get("completada", False)


def leccion_puntaje(progreso: dict, nivel: int, num: int):
    return progreso.get("lecciones", {}).get(_clave(nivel, num), {}).get("puntaje")


def leccion_desbloqueada(progreso: dict, nivel: int, num: int) -> bool:
    """The 1st lesson of EACH level is always open. Each following
    lesson (within the same level) unlocks upon completing the
    immediately preceding one."""
    if num == 1:
        return True
    orden = _orden_lecciones()
    idx = orden.index((nivel, num))
    nivel_ant, num_ant = orden[idx - 1]
    return leccion_completada(progreso, nivel_ant, num_ant)


def marcar_leccion_completada(usuario: str, nivel: int, num: int, puntaje: int = 100):
    """Saves a lesson as completed for `usuario` and returns the
    updated progress. If it was already completed, it only updates the
    score if the new one is better (doesn't add points again)."""
    if usuarios_col is None or not usuario:
        return obtener_progreso(usuario)

    progreso = obtener_progreso(usuario)
    clave = _clave(nivel, num)
    existia = progreso["lecciones"].get(clave)

    if existia and existia.get("completada"):
        mejor_puntaje = max(puntaje, existia.get("puntaje", 0))
        progreso["lecciones"][clave]["puntaje"] = mejor_puntaje
    else:
        progreso["lecciones"][clave] = {
            "completada": True,
            "puntaje": puntaje,
            "fecha": datetime.now(timezone.utc).isoformat(),
        }
        progreso["puntos"] = progreso.get("puntos", 0) + PUNTOS_POR_LECCION

    usuarios_col.update_one({"nombre": usuario}, {"$set": {"progreso": progreso}})
    return progreso


def total_lecciones() -> int:
    return len(_orden_lecciones())


def contar_completadas(progreso: dict) -> int:
    return sum(1 for v in progreso.get("lecciones", {}).values() if v.get("completada"))


def porcentaje_general(progreso: dict) -> int:
    total = total_lecciones()
    if total == 0:
        return 0
    return round(contar_completadas(progreso) / total * 100)


def porcentaje_nivel(progreso: dict, nivel: int) -> int:
    lecciones = NIVELES.get(nivel, [])
    if not lecciones:
        return 0
    hechas = sum(1 for num in lecciones if leccion_completada(progreso, nivel, num))
    return round(hechas / len(lecciones) * 100)
