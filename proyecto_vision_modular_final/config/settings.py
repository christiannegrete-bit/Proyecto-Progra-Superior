"""
El archivo settings.py centraliza toda la configuración del proyecto.
    1-Primero carga el archivo .env con _load_env_file.
    2-Luego, con _get, convierte cada valor a su tipo correcto y expone variables globales limpias 
    que el resto del sistema usa.
    3-Finalmente, ensure_paths() valida que todas las rutas definidas en el .env existan antes de 
    arrancar el programa, para evitar errores durante la ejecución.
"""
import os
from typing import Callable, Any, Dict


def _load_env_file(path: str = ".env") -> Dict[str, str]:
    """Carga un archivo .env simple KEY=VALUE sin dependencias externas."""
    env: Dict[str, str] = {}
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No se encontró el archivo .env en {os.path.abspath(path)}"
        )

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            env[key.strip()] = value.strip()

    return env


_ENV = _load_env_file(".env")


def _get(name: str, cast: Callable[[str], Any]):
    """Obtiene un valor desde .env y lo castea al tipo correcto."""
    raw = _ENV.get(name)
    if raw is None:
        raise KeyError(f"Variable requerida '{name}' no está definida en .env")

    try:
        return cast(raw)
    except Exception:
        raise ValueError(f"El valor de '{name}' en .env no pudo convertirse correctamente.")

# ================== VALORES EXTRAÍDOS DEL .env ==================

SAVEDMODEL_DIR = _get("SAVEDMODEL_DIR", str)
IMG_DIR        = _get("IMG_DIR", str)
EXCEL_PATH     = _get("EXCEL_PATH", str)

NO_OBJECT_CLASS = _get("NO_OBJECT_CLASS", str)
THRESHOLD       = _get("THRESHOLD", float)
CONFIRM_FRAMES  = _get("CONFIRM_FRAMES", int)
INPUT_SIZE      = _get("INPUT_SIZE", int)
CAM_INDEX       = _get("CAM_INDEX", int)
FRAME_W         = _get("FRAME_W", int)
FRAME_H         = _get("FRAME_H", int)


def ensure_paths() -> None:
    """Verifica rutas críticas y detiene el programa si algo está mal."""
    if not os.path.isdir(os.path.dirname(SAVEDMODEL_DIR)):
        raise FileNotFoundError(f"Ruta inválida en .env → SAVEDMODEL_DIR = {SAVEDMODEL_DIR}")

    if not os.path.isdir(IMG_DIR):
        raise FileNotFoundError(f"Ruta inválida en .env → IMG_DIR = {IMG_DIR}")

    excel_dir = os.path.dirname(EXCEL_PATH)
    if not os.path.isdir(excel_dir):
        raise FileNotFoundError(f"Ruta inválida en .env → EXCEL_PATH = {EXCEL_PATH}")
