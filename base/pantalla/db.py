"""Central MongoDB connection and user helpers, shared across the whole app.

Before, each screen opened its own connection to Mongo (duplicated). Now all
screens (login, lessons, stats, profile, progress...) import from here to have
a single source of truth.

IMPORTANT: every file in the project must import this module the exact same
way (e.g. always `from pantalla.db import ...`). If different files import it
with different paths (`from db import ...` vs `from pantalla.db import ...`),
Python treats them as separate modules and creates a NEW MongoClient (and a
new connection pool) for each one -- this is the most common cause of
"nearing connection limit" warnings in Atlas.
"""

import atexit
import hashlib
import os
import re
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, PyMongoError
from bson.errors import BSONError

# ── MongoDB ──
MONGO_URI = os.getenv("MONGO_URI", "")

client = None
usuarios_col = None

if MONGO_URI:
    try:
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            # Small desktop app -- a handful of connections is plenty. Keeping
            # this low means that even if this module ever gets imported more
            # than once by mistake, it won't be able to eat the whole 500-
            # connection Atlas free-tier limit on its own.
            maxPoolSize=10,
            minPoolSize=0,
            maxIdleTimeMS=30000,
        )
        client.admin.command("ping")
        db = client["dixlearn"]
        usuarios_col = db["usuarios"]
        usuarios_col.create_index("nombre", unique=True)
        print("✅ Connected to MongoDB Atlas")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
        client = None
        usuarios_col = None
else:
    print("⚠️ MONGO_URI no configurada; funciones de usuario deshabilitadas")

# Make sure the connection (and its whole pool) is released the moment the
# app process exits, instead of lingering until Atlas eventually times it out.
atexit.register(lambda: client.close() if client is not None else None)


def progreso_vacio() -> dict:
    """Progress structure that every new account starts with."""
    return {
        "puntos": 0,
        "racha_dias": 0,
        "lecciones": {},   # "nivel-num": {"completada": bool, "puntaje": int, "fecha": iso}
    }


# ── Helpers de contraseña ────────────────────────────────────────────────────
def hash_password(p: str) -> str:
    return hashlib.sha256(p.encode()).hexdigest()


def verificar_password(pwd: str, hashed: str) -> bool:
    return hash_password(pwd) == (hashed or "").strip().lower()


# ── Helpers de usuario ────────────────────────────────────────────────────────
def obtener_usuario(nombre: str):
    """Looks up a user by name.

    Returns None both when the DB is unreachable AND when Mongo returns a
    document it can't decode (e.g. InvalidBSON). Before, that second case
    raised an uncaught exception that crashed the whole screen -- now the
    app can fall back to treating it like "no data yet" instead of dying.
    """
    if usuarios_col is None:
        return None
    try:
        return usuarios_col.find_one({"nombre": nombre})
    except (PyMongoError, BSONError) as ex:
        print(f"⚠️ Error reading user '{nombre}' from MongoDB: {ex}")
        return None


def registrar_usuario(nombre: str, apellido: str, password: str, correo: str) -> tuple[bool, str]:
    if usuarios_col is None:
        return False, "No connection to the database."
    try:
        usuarios_col.insert_one({
            "nombre":     nombre,
            "apellido":   apellido,
            "contrasena": hash_password(password),
            "correo":     correo.strip().lower(),
            "foto":       None,
            "progreso":   progreso_vacio(),
        })
        return True, "ok"
    except DuplicateKeyError:
        return False, "This user already exists."
    except (PyMongoError, BSONError) as ex:
        return False, f"Error: {ex}"


def actualizar_usuario(nombre: str, cambios: dict) -> tuple[bool, str]:
    """Updates fields in the user's document (profile, password, photo, etc.)."""
    if usuarios_col is None:
        return False, "No connection to the database."
    try:
        usuarios_col.update_one({"nombre": nombre}, {"$set": cambios})
        return True, "ok"
    except (PyMongoError, BSONError) as ex:
        return False, f"Error: {ex}"


def renombrar_usuario(nombre_actual: str, nombre_nuevo: str) -> tuple[bool, str]:
    """Changes a user's 'nombre' (used as the unique identifier)."""
    if usuarios_col is None:
        return False, "No connection to the database."
    if nombre_actual == nombre_nuevo:
        return True, "ok"
    try:
        if usuarios_col.find_one({"nombre": nombre_nuevo}):
            return False, "That username is already taken."
        usuarios_col.update_one({"nombre": nombre_actual}, {"$set": {"nombre": nombre_nuevo}})
        return True, "ok"
    except (PyMongoError, BSONError) as ex:
        return False, f"Error: {ex}"


def correo_valido(correo: str) -> bool:
    correo = (correo or "").strip().lower()
    if not correo or " " in correo:
        return False
    return bool(re.match(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9\-]+(\.[a-zA-Z0-9\-]+)*\.[a-zA-Z]{2,}$", correo))
