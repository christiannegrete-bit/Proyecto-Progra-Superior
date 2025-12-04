'''
La aplicación principal que integra todos los módulos para el sistema de inventario con visión 
por computadora.
    1.-Carga la configuración desde settings.py.
    2.-Inicializa la cámara, el modelo, el preprocesador, el repositorio de inventario y la UI 
    de detalle.
    3.-Crea el motor de inferencia y el controlador de la aplicación.
    4.-Arranca el bucle principal de la aplicación, manejando errores globales para evitar 
    fallos silenciosos.      
'''

from tkinter import Tk

from config.settings import (
    SAVEDMODEL_DIR,
    EXCEL_PATH,
    CAM_INDEX,
    FRAME_W,
    FRAME_H,
    INPUT_SIZE,
    THRESHOLD,
    NO_OBJECT_CLASS,
    CONFIRM_FRAMES,
    ensure_paths,
    MODEL_BACKEND,
    GCLOUD_CREDENTIALS,
    INVENTORY_BACKEND,
    GSHEET_ID,
    GSHEET_WORKSHEET,
    GSHEET_CREDENTIALS,
)

from core.inference.inference_engine import InferenceEngine, load_labels
from core.preprocessing.Tm_preprocessor import TMPreprocessor

from infrastructure.camera.opencv_camera import OpenCVCamera
from infrastructure.model.Tm_saved_model import TMSavedModel
from infrastructure.model.google_vision_model import GoogleVisionModel

from infrastructure.repo.excel_inventory_repo import ExcelInventoryRepo
from infrastructure.repo.google_sheet_inventory_repo import GoogleSheetInventoryRepo

from ui.tk_detail_ui import TkDetailUI
from app.controller import AppController


def main() -> None:
    try:
        # Verificación básica de rutas y configuración
        ensure_paths()

        # --- Inicialización de UI base ---
        root = Tk()
        root.withdraw()

        # --- Dispositivos / infraestructura ---
        camera = OpenCVCamera(index=CAM_INDEX, width=FRAME_W, height=FRAME_H)
        preprocessor = TMPreprocessor(INPUT_SIZE)

        # --- Backend de inventario: excel o google_sheet ---
        if INVENTORY_BACKEND == "excel":
            repo = ExcelInventoryRepo(EXCEL_PATH)
        elif INVENTORY_BACKEND == "google_sheet":
            repo = GoogleSheetInventoryRepo(
                spreadsheet_id=GSHEET_ID,
                worksheet_name=GSHEET_WORKSHEET,
                credentials_path=GSHEET_CREDENTIALS,
            )
        else:
            raise ValueError(
                f"[main] INVENTORY_BACKEND inválido: {INVENTORY_BACKEND!r}. "
                "Usa 'excel' o 'google_sheet'."
            )

        detail_ui = TkDetailUI(root=root, repo=repo)

        # --- Carga de etiquetas / clases ---
        class_names = load_labels(SAVEDMODEL_DIR)

        # --- Backend de modelo: local (SavedModel) o google (Vision API) ---
        if MODEL_BACKEND == "local":
            model = TMSavedModel(SAVEDMODEL_DIR)
        elif MODEL_BACKEND == "google":
            model = GoogleVisionModel(
                credentials_path=GCLOUD_CREDENTIALS,
                class_names=class_names,
            )
        else:
            raise ValueError(
                f"[main] MODEL_BACKEND inválido: {MODEL_BACKEND!r}. "
                "Usa 'local' o 'google'."
            )

        # --- Motor de inferencia ---
        engine = InferenceEngine(
            preprocessor=preprocessor,
            model=model,
            class_names=class_names,
        )

        # Las primeras N clases se consideran válidas para inventario
        valid_classes = set(class_names[:4])

        # --- Controlador principal de la app ---
        controller = AppController(
            camera=camera,
            engine=engine,
            ui=detail_ui,
            class_names=class_names,
            valid_classes=valid_classes,
            no_object_class=NO_OBJECT_CLASS,
            threshold=THRESHOLD,
            confirm_frames=CONFIRM_FRAMES,
        )

        controller.run(root)

    except Exception as e:
        print(f"[ERROR] Ha ocurrido un error en la aplicación principal: {e}")


if __name__ == "__main__":
    main()
